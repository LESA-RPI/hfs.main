# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:52:36 2022

@author: Dru Ellering
"""

import math
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

class Layout:
    # Return the LED parameters of LED n
    def get(self, led_id):
        return (self.leds[led_id], self.lenses[led_id], self.adjusted_points[led_id])
    
    # Center the layout for the current image size
    def shift(self, size):
        # Find the center of the given points
        avg_x = avg_y = 0
        for point in self.points:
            avg_x += point[0]
            avg_y += point[1]
        center = (round(avg_x / len(self.leds)), round(avg_y / len(self.leds)))
        # Find the center of the image
        self.center = (round(size[0] / 2), round(size[1] / 2))
        # Center all points and add them to the adjusted point list
        self.adjusted_points = []        
        for point in self.points:
            x = round((point[0] - center[0] + self.center[0]))
            y = round((point[1] - center[1] + self.center[1]))
            self.adjusted_points.append((x, y))

class SimpleLayout(Layout):
    def __init__(self, points_mm, leds, lenses):
        self.leds = leds
        self.points = points_mm
        self.lenses = lenses
        self.center = (0,0)
    
class CircularLayout(Layout):
    def __init__(self, radius_mm, leds, lenses):
        self.points = []
        self.center = (0,0)
        # Make the layout with the given parameters
        count = len(leds)
        degree = 360 / count 
        for n in range(count):
            theta = math.radians(degree * n)
            x = math.cos(theta) * radius_mm
            y = math.sin(theta) * radius_mm
            self.points.append((x, y))
        self.leds = leds
        self.lenses = lenses


class Lens:
    def __init__(self, efficiency, fwhm, curve):
        # Convert FWHM to beam angle in Sr
        self.beam_angle = (2 * math.pi * (1 - math.cos(math.radians(fwhm / 2))))
        self.efficiency = efficiency
        # Estimate the equation of angular distribution for the lens
        # Start by adding all of the given data points
        pts, xs, ys = [], [], []
        for key, value in curve.items():
            pts.append((key, value))
            pts.append((180-key, value))
        pts.sort()
        for point in pts:
            xs.append(point[0])
            ys.append(point[1])
        # Use scipy.curve_fit to to get the estimated function
        param, covariance = curve_fit(self._bellCurve, xs, ys, (90, 15, 0.2))
        # Display the plot
        self.mean, self.sigma, self.var1 = param
        plt.plot(xs, ys, 'o')
        plt.plot(range(0,180), self._bellCurve(range(0,180), self.mean, self.sigma, self.var1))
        
    # Basic function for scipy to use
    # https://www.wallstreetmojo.com/bell-curve/
    def _bellCurve(self, x, mean, sigma, var1):
        global a
        y = []
        for val in x:
            e1 = 1 / (sigma * math.sqrt(2 * math.pi))
            e2 = ((val - mean) / var1) * ((val - mean) / var1)
            e3 = math.exp(-e2/(2*sigma*sigma))
            y.append(e1 * e3)
        return y
    
    # Return the scaling parameter for a light source viewed at a specific angle
    def getScalar(self, angle):
        # Calculate the bell curve
        e1 = 1 / (self.sigma * math.sqrt(2 * math.pi))
        e2 = ((angle - self.mean) / self.var1) * ((angle - self.mean) / self.var1)
        e3 = math.exp(-e2/(2*self.sigma*self.sigma))
        # Result must be within [0, 1]
        return max(0, min(1, e1 * e3))

class LED:
    def __init__(self, power_mW, wavelength, drive_factor):
        self.power = (power_mW / 1000) * drive_factor
        self.wavelength = wavelength
        # Set the photon const (a shortcut to calculate the flux)
        self.photon_const = 0.00836 * wavelength
        
    # Get the photon flux in umol/(m2*s)
    def getFlux(self, distance_m, beam_angle, efficiency):
        irradiance = self.getIrradiance(distance_m, beam_angle, efficiency)
        return self.photon_const * irradiance
    
    # Get the power in W
    def getPower(self, distance_m, beam_angle, efficiency, unit):
        irradiance = self.getIrradiance(distance_m, beam_angle, efficiency)
        return (irradiance / (unit ** 2)) # W
    
    # Get the irradiance in W/m2
    def getIrradiance(self, distance_m, beam_angle, efficiency):
        beam_area = (distance_m ** 2) * beam_angle
        # Multiply final power by 0.5 because only 50% of the power is in the fwhm
        irradiance = (efficiency * self.power * 0.5) / beam_area
        return irradiance
    
class Photodiode:
    def __init__(self, responsivity_A_W, dark_current_mA, detection_area_mm2, photodiode_circuit, max_value = 4095):
        self.responsivity = responsivity_A_W # A/W
        self.dark_current = dark_current_mA # mA
        self.detection_area = detection_area_mm2 # mm2
        self.max_value = max_value
        # Finish setting up the photodiode
        self._setup(photodiode_circuit)
        self.circuit = photodiode_circuit
    
    # Delete this function
    def getEstimatedPower(self, height_mm, fluorescence_factor, power_on_canopy_mW):
        approx_diode_diameter = 2 * math.sqrt(self.detection_area / math.pi)
        # Get the approximate power on the photodiode using Lambert's cosine law,
        # where the area under the cos curve (given by the sin curve) at a particular
        # angle is the power factor
        power_factor = math.sin(math.atan(approx_diode_diameter / height_mm)) 
        return power_on_canopy_mW * power_factor * fluorescence_factor # mW

    # Delete this function
    def getEstimatedCurrent(self, height_mm, fluorecence_factor, power_on_canopy_mW):
        power = self.getEstimatedPower(height_mm, fluorecence_factor, power_on_canopy_mW) # mW
        return (power * self.responsivity) # mA

    # Convert the power on the photodiode to the photodiode current
    def getCurrent(self, power_mW):
        return (power_mW * self.responsivity) # mA
    
    # Delete this function
    def getEstimatedValue(self, height_mm, fluorecence_factor, power_on_canopy_mW):
        return round(min(self.getEstimatedCurrent(height_mm, fluorecence_factor, power_on_canopy_mW) / self.conversion_factor, self.max_value))
    
    # Convert the power on the photodiode to the reported microcontroller value
    def getValue(self, power_mW):
        return round(min(self.getCurrent(power_mW) / self.conversion_factor, self.max_value))

    # Setup the photodiode with the proper resistors
    def _setup(self, photodiode_circuit):
        voltage_gain = (photodiode_circuit.r_op07_kohm / 10) + 1
        output_ad620_mv = (1000 * photodiode_circuit.max_photodiode_voltage) / voltage_gain
        output_photodiode_mv = output_ad620_mv / ((49400 / photodiode_circuit.r_ad620_ohm) + 1)
        output_photodiode_uA = output_photodiode_mv / photodiode_circuit.r_photodiode_kohm
        self.max_current_mA = output_photodiode_uA / 1000
        self.conversion_factor = output_photodiode_uA / self.max_value

class Circuit:
    def __init__(self, max_photodiode_voltage, r_photodiode_kohm, r_op07_kohm, r_ad620_ohm):
        self.max_photodiode_voltage = max_photodiode_voltage
        self.r_photodiode_kohm = r_photodiode_kohm
        self.r_op07_kohm = r_op07_kohm
        self.r_ad620_ohm = r_ad620_ohm
        
# The unit scale to use
class Unit:
    Meter = 1
    Centimeter = 100
    Milimeter = 1000

# The options to pass into simulations
class Options:
    unit = Unit.Milimeter

    cutoff_diameter = 72 # mm
    img_size = (300, 300)
    img_center = (150, 150)

    photodiode_offset = 0
    fluorescence_factor = 0.04
    
    max_value = 4095
    #max_photodiode_voltage = 3.3 # V
    #r_ad620_ohm = 220
    #r_photodiode_kohm = 100
    #r_op07_kohm = 200
    
    shield_top_radius = 36.5 # mm
    diode_to_shield_height = 70.5 # mm
    LED_to_shield_height = 0 # mm

    def init(self, height):
        self.cutoff_diameter = 2 * self.shield_top_radius * (self.diode_to_shield_height + height) / self.diode_to_shield_height
        width = math.ceil(self.cutoff_diameter / (1000 / self.unit))
        self.img_center = (width / 2, width / 2)
        self.img_size = (width, width)

    def getLedHeight(self, height):
        return self.LED_to_shield_height + height
        
    def getDiodeHeight(self, height):
        return self.diode_to_shield_height + height # mm

LambertianSource = Lens(1, 120, {90: 1, 75: 0.9659, 60: 0.866, 45: 0.707, 30: 0.5, 15: 0.2588, 0: 0})