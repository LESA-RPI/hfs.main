# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:55:59 2022

@author: Dru Ellering
"""

from classes import *
from simulations import *
import csv
import math

# LEDs
blue_xpe2 = LED(power_mW = 43000/40, wavelength = 475, drive_factor = 1.7)
royal_blue_rebel = LED(power_mW = 840, wavelength = 447.5, drive_factor = 1)

# Lenses
carlco_10412_xpe2 = Lens(efficiency = 0.92, fwhm = 14, curve = {90: 1, 83: 0.5, 65: 0})
#carlco_10003_xpe2 = Lens(efficiency = 0.885, beam_angle = 1 / 35.4, curve = {90: 1, 86.55: 0.5 ,84: 0.1, 80: 0.04, 70: 0})
iac_rebel = Lens(efficiency = 0.896, fwhm = 18, curve = {90: 1, 85: 0.73, 81.015: 0.5})

# Layouts
HFS_layout1 = CircularLayout(radius_mm = 55 / 2, leds = [blue_xpe2] * 12, lenses = [carlco_10412_xpe2] * 12)
FUSSy_layout = SimpleLayout(points_mm = [(0,0), (10,0), (5,10), (0,22), (10,22), (5,32), (39,0), (49,0), (44,10), (39,22), (49,22), (44,32)], leds = [royal_blue_rebel] * 12, lenses = [iac_rebel] * 12)

# Circuits
circuit_HFS1 = Circuit(max_photodiode_voltage = 3.3, r_photodiode_kohm = 100, r_op07_kohm = 200, r_ad620_ohm = 220)

# Photodiodes
TO8 = Photodiode(responsivity_A_W = 0.4, dark_current_mA = 0.000012, detection_area_mm2 = 42, photodiode_circuit = circuit_HFS1)

# HFS options
options_HFS = Options()
options_HFS.max_value = 4095
options_HFS.shield_top_radius = 36.5 # mm
options_HFS.diode_to_shield_height = 70.5 # mm
options_HFS.LED_to_shield_height = 68.1 # mm
options_HFS.unit = Unit.Milimeter
options_HFS.fluorescence_factor = 0.02

# FUSSy options
options_FUSSy = Options()
options_FUSSy.cutoff_diameter = 120

# Simulate
# returns [microcontroller_value, sensing_area, flux_avg, flux_std_dev]
simulateDesign(options_HFS, 520, HFS_layout1, TO8, True, False)
#simulateDesign(options_HFS, 520, FUSSy_layout, TO8, True, False)

# Calculate the photodiode current
# returns [sensing_area, chlf_normal, chlf_std, f_factor, diode_current, diode_voltage]
#simulateIdealDevice(options_HFS, HFS_layout1, TO8, height = 275, microcontroller_value = 3750)
#simulateIdealDevice(options_HFS, HFS_layout1, TO8, height = 300, microcontroller_value = 3265)
#simulateIdealDevice(options_HFS, HFS_layout1, TO8, height = 600, microcontroller_value = 1001)
#simulateIdealDevice(options_HFS, HFS_layout1, TO8, height = 1200, microcontroller_value = 279)

def writeToSpreadsheet(_min, _max, skip):
    with open('data_out.csv', 'w', newline = '') as file:
        filewriter = csv.writer(file)
        filewriter.writerow(['Height (mm)', 'Microcontroller Value', 'Sensing Area (mm2)', 'Average Flux (umol/m2*s)', 'Standard Deviation of Flux (umol/m2*s)', 'Sensing Area (mm2)', 'Normalized ChlF (%)', 'Constant (K)', 'Fluorescence Quantum Yield', 'Photodiode Current (uA)', 'Photodiode Voltage (mV)', 'Total Canopy Flux (umol/m2*s)', 'Photodiode Ideal Power (mW)', 'Normalized ChlF', 'Estimated Fluorescence Quantum Yield'])
        # height from _min to _max
        for n in range(round(_min / skip), round(_max / skip)):
            height = (n * skip)
            data1 = simulateDesign(options_HFS, height, HFS_layout1, TO8, False, False)
            microcontroller_value = data1[0]
            data2 = simulateIdealDevice(options_HFS, HFS_layout1, TO8, height = height, microcontroller_value = microcontroller_value, printing = False)
            data3 = simulateDevice(options_HFS, HFS_layout1, TO8, height = height, microcontroller_value = microcontroller_value, printing = False)
            data = [height] + data1 + data2 + [data3[1], data3[2]]
            for i in range(len(data)):
                data[i] = str(data[i])
            filewriter.writerow(data)
            print('height: ' + str(height) + 'mm')
            
#writeToSpreadsheet(0, 5000, skip = 1)





