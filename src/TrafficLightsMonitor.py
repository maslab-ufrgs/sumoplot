#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy
from operator import eq, ge, gt, attrgetter
from Constants import *
from HelpFunctions import formatListOutput

class TrafficLightsMonitor(object):
    """Class responsible for handling a set of traffic lights, and allowing 
    selections about the same.
    """

    def __init__(self):
        """Keeps every necessary traffic lights used in the simulation. """
        self._trafficLightsDict = {}
        """Keeps for each case possible, the lists of identifiers of traffic 
        lights that must be in the simulation output.
        """
        self._trafficLightsIdOutputDict = {}
        """Keeps the minimum step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum step length of the simulation."""
        self._maxStep = 0
        """Keeps the actual limit step length of the simulation."""
        self._steps = 0

    @property
    def minStep(self):
        """Return the minimum step length of the simulation as an integer."""
        return self._minStep

    @minStep.setter
    def minStep(self, minStep):
        """Overwrite the minimum step length of the simulation."""
        self._minStep = minStep

    @property
    def maxStep(self):
        """Return the maximum step length of the simulation as an integer."""
        return self._maxStep

    @maxStep.setter
    def maxStep(self, maxStep):
        """Overwrite the maximum step length of the simulation."""
        self._maxStep = maxStep

    @property
    def trafficLightsDict(self):
        """Return the the dictionary that keeps the traffic lights used in the 
        simulation.
        """
        return copy.deepcopy(self._trafficLightsDict)

    @trafficLightsDict.setter
    def trafficLightsDict(self, trafficLightsDict):
        """Overwrite the the dictionary that keeps the traffic lights used in 
        the simulation.
        """
        self._trafficLightsDict = copy.deepcopy(trafficLightsDict)

    def addTrafficLights(self, trafficLights, key=None):
        """Add one traffic lights object in the key position of the monitor. If key
            is None or absent, then adds in the next free position.

        Keyword arguments:
        trafficLights -- an Traffic Lights object
        key -- an integer that identifies the position in a dictionary

        """
        if eq(key,None) or (not self._trafficLightsDict.has_key(key)):
            key = self.getSize()

        self._trafficLightsDict[key] = copy.deepcopy(trafficLights)

    def getSize(self):
        """Return the integer number of traffic lights dictionaries in the 
        monitor.
        """
        return len(self._trafficLightsDict)

    def addTrafficLightsIdOutput(self, trafficLightsIdList, key):
        """Add a list of traffic lights string identifiers in the dictionary, in
        the position that has been defined by an name constant.

        Keyword arguments:
        trafficLightsIdList -- an list of string identifiers
        key -- an string constant related to Traffic Lights class

        """
        self._trafficLightsIdOutputDict[key] = copy.deepcopy(trafficLightsIdList)

    def getTrafficLightsLanesById(self, trafficLightsId):
        """Get the list of lanes controlled by the traffic lights identified by 
        its id.

        Keyword arguments:
        trafficLightsId -- an string that identifies a traffic lights

        """
        for trafficLights in self._trafficLightsDict.itervalues():
            if eq(trafficLights.id,trafficLightsId):
                return trafficLights.controlledLanes

    def updateTrafficLights(self, timeStep, trafficLightsId, haltingVehicles):
        """Update the traffic lights with the data extracted for simulation for 
        every step time.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation 
        trafficLightsId -- an string that identifies a traffic lights
        haltingVehicles -- an list of integer representing the stopped vehicles

        """
        self._steps += 1
        for key, trafficLights in self._trafficLightsDict.items():
            if eq(trafficLights.id, trafficLightsId):
                # Updates the number of vehicles in the lane in this time step.
                self._trafficLightsDict[key].addHaltingVehiclesOnStep(timeStep, haltingVehicles)

    def toString(self, pattern, separator=' '):
        """Return a string that contains data referring to the traffic lights 
        from simulation.

        Keyword arguments:
        pattern -- some constant defined for the Traffic Lights class
        separator -- the constant defined for string format

        """
        header = ['#TrafficLights']
        data = ['#TimeStep']
        # Adds the header
        for trafficLights in self._trafficLightsDict.values():
            if eq(pattern,TRAFFIC_LIGHT_HALTING):
                if self._trafficLightsIdOutputDict.has_key(pattern):
                    if trafficLights.id in self._trafficLightsIdOutputDict.get(pattern):
                        header.append(separator+trafficLights.id)
                        for num in range(len(trafficLights.controlledLanes)-1):
                            header.append(separator+'-')
                        for lane in trafficLights.controlledLanes:
                            data.append(separator+lane)
        header.append('\n')
        data.append('\n')

        # Adds the data for each time step.
        if (-1 == self.minStep == self.maxStep):
            interval = range(0, self._steps)
        else:
            interval = range(self.minStep, self.maxStep)

        for timeStep in interval:
            data.append('{0}'.format(timeStep))

            for trafficLights in self._trafficLightsDict.values():
                if eq(pattern,TRAFFIC_LIGHT_HALTING):
                    if self._trafficLightsIdOutputDict.has_key(pattern):
                        if trafficLights.id in self._trafficLightsIdOutputDict.get(pattern):
                            for haltingVehicles in trafficLights.getHaltingVehiclesOnStep(timeStep):
                                data.append(separator+'{0}'.format(haltingVehicles))

            data.append('\n')
        header.append(''.join(data))
        return ''.join(header)

    def toStringEvaluate(self,separator=' '):
        """Return a string that contains data referring the average of the 
        traffic lights from simulation.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        saida = []
        header = ['#TrafficLights']
        data = ['#Lanes']
        avgH = ['HaltingVehicles(avg)']
        stdH = ['HaltingVehicles(stdDev)']
        # Adds the data
        for trafficLights in self._trafficLightsDict.values():
            header.append(trafficLights.id)
            for num in range(len(trafficLights.controlledLanes)-1):
                header.append('-')
            for lane in trafficLights.controlledLanes:
                data.append(lane)
            for val in trafficLights.average(TRAFFIC_LIGHT_HALTING):
                avgH.append('{0:.6f}'.format(val))
            for val in trafficLights.standardDeviation(TRAFFIC_LIGHT_HALTING):
                stdH.append('{0:.6f}'.format(val))

        saida.append(separator.join(header))
        saida.append(separator.join(data))
        saida.append(separator.join(avgH))
        saida.append(separator.join(stdH))

        return '\n'.join(saida)

    def debug(self):
        """An standardized output for verification."""
        data = []
        for trafficLights in self.trafficLightsDict.values():
            data.append(trafficLights.debug())
        return '\n###\n'.join(data)