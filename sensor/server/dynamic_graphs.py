# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 13:56:11 2022
@author: Dru Ellering
"""

import matplotlib.pyplot as plt
from os.path import exists
from matplotlib.dates import (AutoDateLocator, DateFormatter)
from datetime import datetime
import random
import pickle
import copy


# colors
# https://lospec.com/palettes/downgraded-32/og-thumbnail.png
colors = []

colors = ['#f2a561', '#fcef8d', '#b1d480', '#80b878', '#658d78',
          '#7b334c', '#a14d55', '#c77369', '#e3a084', '#f2cb9b', '#d37b86', 
          '#72b6cf', '#5c8ba8', '#4e6679', '#464969', '#44355d',
          '#3d003d', '#621748', '#942c4b', '#c7424f', '#e06b51',
          '#af5d8b', '#804085', '#5b3374', '#412051', '#5c486a', '#887d8d',
          '#dddda0', '#89d9d9','#b8b4b2', '#dcdac9', '#dddda0'
]

# Change click to buttons
# Most recent values display on left

class RTGraph:
    def __init__(self, width, max_height, title, ylabel):
        plt.style.use('ggplot')
        self.max_height= max_height
        self.ylabel = ylabel
        self.num_sensors = 32 # maximum number of sensors
        self.title = title
        self.width = width
        self.path = title.lower().replace(' ', '_')
        if exists("/usr/local/src/hfs/public/" + self.path + ".pickle"):
            self.load()
            return

        # y values
        self.ydata = [None] * self.num_sensors
        self.xdata = [None] * self.num_sensors
        self.sensors = [None] * self.num_sensors
        # x values
        self.min_time = datetime.min
        self.max_time = datetime.min
        
        self._setupFig()
        
        #plt.show()

        
    def _setupFig(self):
        #plt.figure(self.title)
        # Setup this figure
        self.fig, self.fig_axis = plt.subplots(1, 1, figsize = (12, 8), num = self.title, dpi = 200)
        self.fig_axis.set_ylim(0, self.max_height)
        self.fig.set_dpi(600.0)


        # https://matplotlib.org/devdocs/gallery/ticks/date_formatters_locators.html
        self.fig_axis.xaxis.set_major_locator(AutoDateLocator(maxticks = 4, minticks = 4))
        self.fig_axis.xaxis.set_major_formatter(DateFormatter('%a %H:%M.%S'))
        
        # label the graph
        #plt.figure(self.title)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
            
    def save(self):
        path = '/usr/local/src/hfs/public/' + self.path
        try:
            self.fig.savefig(path + '.jpg')
            with open(path + '.pickle', 'wb+') as file:
                pickle.dump(self, file)
        except Exception as err:
            pass
        
        
    def load(self):
        path = '/usr/local/src/hfs/public/' + self.path
        with open(path + '.pickle', 'rb+'):
            obj = pickle.load(file)
        
        self.ydata = copy.deepcopy(obj.ydata)
        self.xdata = copy.deepcopy(obj.xdata)
        self.sensors = copy.deepcopy(obj.sensors)
        self.min_time = copy.deepcopy(obj.min_time)
        self.max_time = copy.deepcopy(obj.max_time)
        
        self._setupFig()
        
        for sid in range(len(obj.sensors)):
            if obj.sensors[sid] is None:
                continue
            self.sensors[sid],  = self.fig_axis.plot(self.xdata[sid], self.ydata[sid], lw = 3, color = colors[sid])
        sensor_count = sum(x is not None for x in self.sensors)
        
        self.fig_axis.legend(self.sensors[:sensor_count], [('Sensor #' + str(i)) for i in range(sensor_count)], fontsize = 'small', bbox_to_anchor = (1, 1), loc = 'upper left')
        plt.table(cellText = list(filter(lambda item: item is not None, self.ydata)),
                        rowLabels=[('Sensor #' + str(i)) for i in range(sensor_count)],
                        colLabels=self.xdata,
                        loc='bottom')
        
        plt.show()
        
    def _updateMinTime(self):
        self.min_time = self.xdata[0][0]
        for sid in range(1, self.num_sensors - 1):
            if self.xdata[sid] is None:
                continue
            if self.xdata[sid][0] < self.min_time:
                self.min_time = self.xdata[0][sid]
    
    def _update(self, timestamp, sid, val):
        # update the timestamp
        if timestamp > self.max_time:
            self.max_time = timestamp
            self._updateMinTime()
            self.fig_axis.set_xlim(self.min_time, self.max_time)
            #self.fig_axis.xaxis.set_major_locator(AutoDateLocator(maxticks = 4, minticks = 4))
            #self.fig_axis.xaxis.set_major_locator(AutoDateLocator(maxticks = 4, minticks = 4))
            #self.fig_axis.locator_params(axis='x', nbins=3)
            #self.fig_axis.locator_params(nbins=4,axis='x')
           
        # add the new value
        self.xdata[sid].append(timestamp)
        self.ydata[sid].append(val)
        
        # remove the old values if they are outside of the save window
        while len(self.ydata[sid]) > self.width:
            self.ydata[sid].pop(0)
            self.xdata[sid].pop(0)
            
        # update the data on the graph
        self.sensors[sid].set_xdata(self.xdata[sid])
        self.sensors[sid].set_ydata(self.ydata[sid])
        
        
    def _setup(self, timestamp, sid, val):
        # set the current figure
        plt.figure(self.title)
        # plot the data
        self.xdata[sid] = [timestamp]
        self.ydata[sid] = [val]
        self.sensors[sid],  = self.fig_axis.plot(self.xdata[sid], self.ydata[sid], lw = 3, color = colors[sid])
        self.sensors[sid].set_label('Sensor ' + str(sid))
        #self.fig_axis.legend(fontsize = 'small', bbox_to_anchor = (1, 1), loc = 'upper left')
        
    def update(self, timestamp, sid, val):
        if self.ydata[sid] is None:
            return self._setup(timestamp, sid, val)
        self._update(timestamp, sid, val)
        
###############
# Sample Code #
###############

# number of samples from EACH sensor we want to save
samples = 100

# make the graphs
graph_raw = RTGraph(samples, 4095, 'Raw Flourescence Data', 'mcu')
graph_norm = RTGraph(samples, 100, 'Normalized Flourescence Data', 'Chlf (%)')
graph_chlf = RTGraph(samples, 100, 'Flourescence Factor Data', 'Flourescence Factor (%)')

# update all graphs at once for convinience
def update(timestamp, sid, val_raw, val_norm, val_chlf):
    graph_raw.update(timestamp, sid, val_raw)
    graph_norm.update(timestamp, sid, val_norm)
    graph_chlf.update(timestamp, sid, val_chlf)

# save all graphs at once for convinience
def save():
    # give the graphs some time to update
    plt.pause(1)
    # save locally
    graph_raw.save()
    graph_norm.save()
    graph_chlf.save()

# feed in some dummy data
#sensors = 10
#vals = [0] * sensors
#for i in range(1000):
#    t = datetime.now()
#    for sid in range(sensors):
#        if i == 0:
#            vals[sid] = random.random()
#        vals[sid] = max(min((random.random() / 100) + vals[sid] - 0.005, 1), 0)
#        
#        # make sure to convert the decimal percentages to actual percentages!
#        update(t, sid, vals[sid] * 4095, 100 * vals[sid], 100 * (vals[sid] ** 2))
#    # save the graphs
#    save()






    