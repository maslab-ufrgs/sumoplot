#!/usr/bin/env python
#-*- coding: utf-8 -*-

from operator import eq
import numpy
import copy
from Constants import *
from HelpFunctions import *

class TrafficLights(object):
    """Class responsible for handling one traffic lights object."""

    def __init__(self, trafficLightsId):
        """Keeps the minimum time step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum time step length of the simulation."""
        self._maxStep = 0
        """Identifies the traffic lights that will be represented by object."""
        self._id = trafficLightsId
        """keeps the logic program(semaphore program) objects that will be used 
        by traffic lights.
        """
        self._logicPrograms = {}
        """keeps the controlled lanes by traffic lights, a lane is part of a 
        edge and connect two nodes.
        """
        self._controlledLanes = []
        """keeps the controlled links by traffic lights, a link is a connection 
        between two lanes at node level.
        """
        self._controlledLinks = []
        """keeps the number of vehicles for each time step and for each lane (an
        list of) that have stopped at the traffic lights.
        """
        self._haltingVehicles = {}

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
    def id(self):
        """Return the identifier of the traffic lights as an string."""
        return self._id

    @id.setter
    def id(self, trafficLightsId):
        """Update the identifier of the traffic lights."""
        self._id = trafficLightsId

    @property
    def logicPrograms(self):
        """Return the dictionary that keeps the semaphore plans for the traffic 
        lights.
        """
        return copy.deepcopy(self._logicPrograms)

    @logicPrograms.setter
    def logicPrograms(self, logicPrograms):
        """Overwrite the dictionary that keeps the semaphore plans for the 
        traffic lights.
        """
        self._logicPrograms = copy.deepcopy(logicPrograms)

    @property
    def controlledLanes(self):
        """Return the list of lanes that are observed by the traffic lights."""
        return copy.deepcopy(self._controlledLanes)

    @controlledLanes.setter
    def controlledLanes(self, controlledLanes):
        """Overwrite the list of lanes that are observed by the traffic lights."""
        self._controlledLanes = copy.deepcopy(controlledLanes)

    @property
    def controlledLinks(self):
        """Return the list of links that are observed by the traffic lights."""
        return copy.deepcopy(self._controlledLinks)

    @controlledLinks.setter
    def controlledLinks(self, controlledLinks):
        """Overwrite the list of links that are observed by the traffic lights."""
        self._controlledLinks = copy.deepcopy(controlledLinks)

    @property
    def haltingVehicles(self):
        """Return the dictionary that keeps the halting vehicles at lanes."""
        return copy.deepcopy(self._haltingVehicles)

    @haltingVehicles.setter
    def haltingVehicles(self, haltingVehicles):
        """Overwrite the dictionary that keeps the halting vehicles at lanes."""
        self._haltingVehicles = copy.deepcopy(haltingVehicles)

    def addLogicProgram(self, logicProgram):
        """Add an logic program into the dictionary that keeps the semaphore 
        plans for the traffic lights.

        Keyword arguments:
        logicProgram -- an Traffic Light Program object

        """
        pos = len(self._logicPrograms)
        self._logicPrograms[pos] = logicProgram

    def getLaneIndex(self, laneId):
        """Return the index position of the indicated lane in the controlled 
        lanes by the traffic lights as an integer.
        
        Keyword arguments:
        laneId -- an string identifier of the lane

        """
        try:
            index = self._controlledLanes.index(laneId)
        except ValueError:
            index = -1

        return index

    def addHaltingVehiclesOnStep(self, timeStep, haltingVehicles):
        """Add halting vehicles list in the referred time step.

        Keyword arguments:
        timeStep -- an integer representing the step
        haltingVehicles -- an list of integer representing the stopped vehicles

        """
        self._haltingVehicles[timeStep] = haltingVehicles

    def hasHaltingVehiclesOnStep(self, timeStep):
        """Return a boolean indicating if the traffic lights has halting 
        vehicles in indicated timeStep.

        Keyword arguments:
        timeStep -- an integer representing the step

        """
        return self._haltingVehicles.has_key(timeStep)

    def getHaltingVehiclesOnStep(self, timeStep):
        """Return the halting vehicles list of the traffic lights in indicated 
        timeStep.

        Keyword arguments:
        timeStep -- an integer representing the step

        """
        if self.hasHaltingVehiclesOnStep(timeStep):
            return self._haltingVehicles[timeStep]
        else:   # default case zero value
            return []

    def addHaltingVehiclesAtLaneOnStep(self, timeStep, haltingVehicles, laneId):
        """Add halting vehicles at lane in the indicated timeStep.

        Keyword arguments:
        timeStep -- an integer representing the step
        haltingVehicles -- an integer representing the number of stopped vehicles
        laneId -- an string identifier for the lane

        """
        if self.hasHaltingVehiclesOnStep(timeStep):
            index = self.getLaneIndex(laneId)
            try:
                self._haltingVehicles[timeStep][index] = haltingVehicles
            except IndexError:
                print "Failed to insert halting vehicles for lane "+str(laneId)+" at "+str(index)+" position and time step "+str(timeStep)

    def hasHaltingVehiclesAtLaneOnStep(self, timeStep, laneId):
        """Return a boolean indicating if the traffic lights has halting 
        vehicles at lane, in indicated timeStep.

        Keyword arguments:
        timeStep -- an integer representing the step
        laneId -- an string identifier for the lane

        """
        if self.hasHaltingVehiclesOnStep(timeStep):
            try:
                self._haltingVehicles[timeStep].index(laneId)
                return True
            except ValueError:
                return False
        else:
            return False

    def getHaltingVehiclesAtLaneOnStep(self, timeStep, laneId):
        """Return the halting vehicles number of the traffic lights in 
        indicated timeStep and lane.

        Keyword arguments:
        timeStep -- an integer representing the step
        laneId -- an string identifier for the lane

        """
        if self.hasHaltingVehiclesAtLaneOnStep(timeStep, laneId):
            index = self.getLaneIndex(laneId)
            return self._haltingVehicles[timeStep][index]
        else:   # default case zero value
            return 0

    def average(self, pattern):
        """Calculate average based on the choice of certain specified pattern,
        that is directly related to measures taken from the simulation and 
        return a list of float.

        Keyword arguments:
        pattern -- some constant defined for the Traffic Lights class

        """
        average = []
        if eq(pattern,TRAFFIC_LIGHT_HALTING):
            for lanes in zip(*self.haltingVehicles.values()):
                average.append(numpy.average(lanes))
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function average()."

        return average

    def standardDeviation(self, pattern):
        """Calculate standard deviation based on the choice of certain specified
        pattern, that is directly related to measures taken from the simulation 
        and return a list of float.

        Keyword arguments:
        pattern -- some constant defined for the Traffic Lights class

        """
        std = []
        if(eq(pattern,TRAFFIC_LIGHT_HALTING)):
            for lanes in zip(*self.haltingVehicles.values()):
                std.append(numpy.std(lanes))
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function standardDeviation()."

        return std

    def toString(self, separator=' '):
        """Return the string that represent the Traffic Lights object.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        data = []
        data.append('#Id='+self.id+'\n')
        
        lanes = []
        for laneId in self.controlledLanes :
            lanes.append(laneId)
        
        data.append('#Lanes='+formatListOutput(lanes)+'\n')
        data.append('#TimeStep')
        
        for laneId in lanes:
            data.append(separator+laneId)
        data.append('\n')

        if (-1 == self.minStep == self.maxStep):
            interval = self.haltingVehicles.keys()
        else:
            interval = range(self.minStep, self.maxStep)

        for timeStep in interval:
            data.append('{0}'.format(timeStep))
            for lane in self.getHaltingVehiclesOnStep(timeStep):
                data.append(separator+'{0}'.format(lane))
            data.append('\n')

        return ''.join(data)

    def debug(self, separator=' '):
        """An standardized output for verification."""
        data = []
        data.append('#Id='+self.id+'\n')
        
        lanes = []
        for laneId in self.controlledLanes:
            lanes.append(laneId)
        data.append('#Lanes='+formatListOutput(lanes)+'\n')

        data.append('#Logic program\n')
        for logicProgram in self.logicPrograms.values():
            data.append(str(logicProgram))

        if (-1 == self.minStep == self.maxStep):
            interval = self.haltingVehicles.keys()
        else:
            interval = range(self.minStep, self.maxStep)

        data.append('#Halting Vehicles\n')
        data.append('#TimeStep')
        for laneId in lanes:
            data.append(separator+'{0}'.format(laneId))
        data.append('\n')
        for timeStep in interval:
            data.append('{0}'.format(timeStep))
            for lane in self.getHaltingVehiclesOnStep(timeStep):
                data.append(separator+'{0}'.format(lane))
            data.append('\n')

        return ''.join(data)
