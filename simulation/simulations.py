# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:05:22 2022

@author: Dru Ellering
"""

import math
import PIL
import statistics
from classes import *

# Calclulate the distance between two points
def distance(p0, p1):
    return math.sqrt(((p0[0] - p1[0]) ** 2) + ((p0[1] - p1[1]) ** 2))

# Calculate the hypotenuse given two legs of a triangle
def hypotenuse(a, b):
    return math.sqrt((a ** 2) + (b ** 2))    

# Code that will run on the device
def simulateDevice(options, layout, photodiode, height, microcontroller_value, printing = True):
    diode_height = options.getDiodeHeight(height)
    
    actual_photodiode_uA = microcontroller_value * photodiode.conversion_factor
    
    sensing_area = ((options.cutoff_diameter / 2) ** 2) * math.pi
    
    k = 21.47858511 # Value from callibration to calculate the chlf_factor
    total_canopy_flux = 582837.181 # Value from calibration, does not need to be very accurate
    average_flux = total_canopy_flux / sensing_area
    
    maximum_photodiode_current = 4095 * photodiode.conversion_factor
    
    # Calculate ChlF values
    chlf_factor = (microcontroller_value * k) / (average_flux * average_flux * diode_height * diode_height)
    #chlf_factor = actual_photodiode_uA / expected_photodiode_current
    chlf_normal = microcontroller_value / options.max_value

    if printing:
        print('')
        print('Sensor Report')
        print('-' * 20)
        
        print('Max allowed photodiode current (uA): ' + str(round(maximum_photodiode_current, 4)))
        print('Actual photodiode current (uA): ' + str(round(actual_photodiode_uA, 6)))
        print('')
        
        print('Fluorescence factor: ' + str(round(chlf_factor, 4)))
        print('Normalized fluorescence: ' + str(round(chlf_normal, 4)))
        print('')
        
        print('Cutoff diameter (cm): ' + str(round(options.cutoff_diameter * 0.1)))
        print('Sensing area (cm2): ' + str(round(sensing_area * 0.01)))
    
    # returns [sensing_area, chlf_normal, f_factor, diode_current, total_canopy_flux]
    return [sensing_area, chlf_normal, chlf_factor, actual_photodiode_uA, total_canopy_flux]

# Simulation code that will exist on the microcontroller to give chlf values
def simulateIdealDevice(options, layout, photodiode, height, microcontroller_value, printing = True):
    # Setup the photodiode and options
    options.init(height)
    led_height = options.getLedHeight(height)
    diode_height = options.getDiodeHeight(height)
    layout.shift((options.img_size[0] * 1000 / options.unit, options.img_size[1] * 1000 / options.unit))
    
    # Calculate the known photodiode values
    actual_photodiode_uA = microcontroller_value * photodiode.conversion_factor
    actual_photodiode_mv = actual_photodiode_uA * photodiode.circuit.r_photodiode_kohm
    
    total_canopy_flux = 0
    photodiode_ideal_power = 0
    # Get the estimated canopy flux and ideal photodiode power by running through the whole simulated area
    for m in range(options.img_size[0]):
        for n in range(options.img_size[1]):
            # Get the coords in mm at the center of the the area
            x = (m * (1000 / options.unit)) + (500 / options.unit)
            y = (n * (1000 / options.unit)) + (500 / options.unit)
            # Since the area is a square, skip any spots that are outside the diameter
            if distance((x, y), layout.center) > options.cutoff_diameter / 2:
                continue
            # Reset the power 
            total_power = 0
            # Gather the power and flux from each LED
            for i in range(len(layout.leds)):
                # Get the LED
                led, lens, point = layout.get(i)
                # Get the distance from
                xy = distance((x, y), point) # mm
                d = hypotenuse(xy, led_height) / 1000 # m
                
                power = led.getPower(d, lens.beam_angle, lens.efficiency, options.unit)
                flux = led.getFlux(d, lens.beam_angle, lens.efficiency)
                a_factor = lens.getScalar(math.degrees(math.atan2(led_height, xy)))
                # Get the power hitting from this area
                total_power += power * a_factor
                total_canopy_flux += flux * a_factor
            
            # Calculate power hitting the photodiode
            center = (options.img_center[0] * (1000 / options.unit), options.img_center[1] * (1000 / options.unit))
            xy = distance((x, y), center) # mm
            d = hypotenuse(xy, diode_height) / 1000 # m
            # Need canopy power in W
            plant = LED(total_power * 1000, 720, 1)
            
            # Multiply by the scaled detection area            
            power = plant.getPower(d, LambertianSource.beam_angle, 1, Unit.Milimeter) # W
            a_factor = LambertianSource.getScalar(math.degrees(math.atan2(diode_height, xy)))
            power *= a_factor * photodiode.detection_area
            photodiode_ideal_power += power
    
    # Finish off some calculations
    photodiode_ideal_power *= 1000 # mW
    sensing_area = ((options.cutoff_diameter / 2) ** 2) * math.pi
    maximum_photodiode_current = 4095 * photodiode.conversion_factor
    expected_photodiode_current = photodiode.getCurrent(photodiode_ideal_power)
    average_flux = total_canopy_flux / sensing_area
    
    # Calculate ChlF values    
    chlf_factor = actual_photodiode_uA / expected_photodiode_current
    constant_k = chlf_factor / (microcontroller_value / (average_flux * average_flux * diode_height * diode_height))
    chlf_normal = microcontroller_value / options.max_value

    # Print
    if printing:
        print('')
        print('Sensor Report')
        print('-' * 20)
        
        print('Max allowed photodiode current (uA): ' + str(round(maximum_photodiode_current, 4)))
        print('Expected photodiode current (uA): ' + str(round(expected_photodiode_current, 6)))
        print('Actual photodiode current (uA): ' + str(round(actual_photodiode_uA, 6)))
        print('Actual photodiode voltage (mV): ' + str(round(actual_photodiode_mv, 4)))
        print('')
        
        print('Fluorescence factor: ' + str(round(chlf_factor, 4)))
        print('Constant (k): ' + str(round(constant_k)))
        print('Normalized fluorescence: ' + str(round(chlf_normal, 4)))
        print('')
        
        print('Cutoff diameter (cm): ' + str(round(options.cutoff_diameter * 0.1)))
        print('Sensing area (cm2): ' + str(round(sensing_area * 0.01)))
    
    # returns [sensing_area, chlf_normal, chlf_std, f_factor, diode_current, diode_voltage, total_canopy_flux, photodiode_ideal_power]
    return [sensing_area, chlf_normal, constant_k, chlf_factor, actual_photodiode_uA, actual_photodiode_mv, total_canopy_flux, photodiode_ideal_power]
    
# Simulation code for designing topdown device design
def simulateDesign(options, height_mm, layout, photodiode, printing = True, show = False):
    # Setup the options, layout, and photodiode with current variables
    options.init(height_mm)
    diode_height = options.getDiodeHeight(height_mm)
    #photodiode.setup(options.max_photodiode_voltage, options.r_photodiode_kohm, options.r_op07_kohm, options.r_ad620_ohm)
    led_height = options.getLedHeight(height_mm)
    layout.shift((options.img_size[0] * 1000 / options.unit, options.img_size[1] * 1000 / options.unit))
    min_flux = math.inf
    max_flux = 0
    # Setup print settings
    if show:
        img = PIL.Image.new(mode = "RGB", size = options.img_size)
        pixels = img.load()
        for m in range(options.img_size[0]):
            for n in range(options.img_size[1]):
                x = (m * (1000 / options.unit)) + (500 / options.unit)
                y = (n * (1000 / options.unit)) + (500 / options.unit)
                if distance((x, y), layout.center) > options.cutoff_diameter / 2:
                    continue
                total_flux = 0
                for i in range(len(layout.leds)):
                    # Get the LED
                    led, lens, point = layout.get(i)
                    # Get the flux at this point
                    xy = distance((x, y), point) # mm
                    d = hypotenuse(xy, led_height) / 1000 # m
                    flux = led.getFlux(d, lens.beam_angle, lens.efficiency)
                    # Get the angular efficnecy at this point
                    a_factor = lens.getScalar(math.degrees(math.atan2(led_height, xy)))
                    total_flux += flux * a_factor
                min_flux = min(min_flux, total_flux)
                max_flux = max(max_flux, total_flux)
    
    # Setup led settings
    ideal_max_flux = 0
    for i in range(len(layout.leds)):
        # Get the LED
        led, lens, point = layout.get(i)
        ideal_max_flux += led.getFlux(led_height / 1000, lens.beam_angle, lens.efficiency)
    
    average_flux = 0
    flux_list = []
    canopy_power = 0
    photodiode_power = 0
    central_flux = 0
    nearest = math.inf
    for m in range(options.img_size[0]):
        for n in range(options.img_size[1]):
            x = (m * (1000 / options.unit)) + (500 / options.unit)
            y = (n * (1000 / options.unit)) + (500 / options.unit)
            if distance((x, y), layout.center) > options.cutoff_diameter / 2:
                if show:
                    pixels[m, n] = (0, 0, 0)
                continue
            
            total_flux = 0
            total_power = 0
            for i in range(len(layout.leds)):
                # Get the LED
                led, lens, point = layout.get(i)
                # Get the flux and intensity at this point
                xy = distance((x, y), point) # mm
                d = hypotenuse(xy, led_height) / 1000 # m
                
                
                flux = led.getFlux(d, lens.beam_angle, lens.efficiency)
                power = led.getPower(d, lens.beam_angle, lens.efficiency, options.unit)
                # Get the angular efficnecy at this point
                a_factor = lens.getScalar(math.degrees(math.atan2(led_height, xy)))
                total_flux += flux * a_factor
                total_power += power * a_factor

            # Get the totals
            flux_list.append(total_flux)
            average_flux += total_flux
            canopy_power += total_power
            # Update central flux
            xy = distance((x, y), layout.center)
            if (xy < nearest):
                nearest = xy
                central_flux = total_flux
            
            # Only do if an image is required
            if show:
                if (x, y) in layout.points:
                    pixels[x, y] = (0, 0, 255)
                else:
                    color = round(((total_flux - (min_flux / 2)) / (max_flux - (min_flux / 2))) * 255)
                    pixels[m, n] = (color, color, color)
            
            # Calculate power hitting the photodiode
            center = (options.img_center[0] * (1000 / options.unit), options.img_center[1] * (1000 / options.unit))
            xy = distance((x, y), center)
            d = hypotenuse(xy, diode_height) / 1000 # mm
            # Need canopy power in mW
            plant = LED(total_power * 1000, 720, 1)
            power = plant.getPower(d, LambertianSource.beam_angle, options.fluorescence_factor, Unit.Milimeter) # W/mm2
            a_factor = LambertianSource.getScalar(math.degrees(math.atan2(diode_height, xy)))
            # Multiply by the scaled detection area
            power *= a_factor * photodiode.detection_area # W
            photodiode_power += power # W

    # Finish the avg flux
    sensing_area = ((options.cutoff_diameter / 2) ** 2) * math.pi
    average_flux /= sensing_area
    
    # Convert the power on canopy
    canopy_power *= 1000 # mW
    photodiode_power *= 1000 # mW
    
    dev = statistics.stdev(flux_list)
    
    microcontroller_value_est = photodiode.getEstimatedValue(diode_height, options.fluorescence_factor, canopy_power)
    microcontroller_value = photodiode.getValue(photodiode_power)

    if printing:
        print('')
        print('Simulation Report')
        print('-' * 20)
        
        print('Ideal max flux: ' + str(round(ideal_max_flux / 10) * 10))
        print('Std flux dev: ' + str(round(dev)))
        print('95% of values fall between: ' + str(max(round((average_flux - (dev * 2)) / 10) * 10, 0)) + ' and '+str(round(((dev * 2) + average_flux) / 10) * 10))
        if show:
            print('Flux max: ' + str(round(max_flux / 10) * 10))
            print('Flux min: ' + str(round(min_flux / 10) * 10))
    
        print('Central flux: ' + str(round(central_flux / 10) * 10))
        print('')
    
        print('Flux avg in area: ' + str(round(average_flux / 10) * 10))
        print('Power on canopy (mW): ' + str(round(canopy_power)))
        print('Sensing area (cm2): ' + str(sensing_area * 0.01))
        print('')
        
        print('Estimated photodiode power (uW): ' + str(round(photodiode_power * 1000, 2)))
        print('Estimated photodiode current (mA): ' + str(round(photodiode.getCurrent(photodiode_power), 6)))
        print('Estimated photodiode current factor: ' + str(round(photodiode.getCurrent(photodiode_power) / photodiode.dark_current, 1)))
        print('Estimated microcontroller value: ' + str(microcontroller_value))
        print('')
    
    # Finish up the image
    if show:
        # Draw a reference grid on the image every 10cm
        for x in range(math.floor(options.img_size[0] / 100)):
            for y in range(math.floor(options.img_size[1])): 
                if (x * d, y) in layout.points: continue
                a = pixels[x * d, y][0]
                pixels[x * d, y] = (255, a, a)
        for x in range(math.floor(options.img_size[0])):
            for y in range(math.floor(options.img_size[1] / 100)):
                if (x, y * d) in layout.points: continue
                a = pixels[x, y * d][0]
                pixels[x, y * d] = (255, a, a)
        # Draw the LEDs
        for point in layout.adjusted_points:
            x = round(point[0] / (1000 / options.unit))
            y = round(point[1] / (1000 / options.unit))
            a = pixels[x, y][0]
            pixels[x, y] = (255, 0, 0)
        # Save and display the image
        img.show() 
        img.save('latest.jpg')
    
    # returns [microcontroller_value, sensing_area, flux_avg, flux_std_dev, ]
    return [microcontroller_value, sensing_area, average_flux, dev]