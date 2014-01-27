#!/usr/bin/env python
#-*- coding: utf-8 -*-

from operator import eq
import numpy
import copy
from Constants import *

class Edge(object):
    """Class responsible for handling one edge object."""

    def __init__(self, edgeId, fromNode, toNode, length, verbose=False):
        """Keeps the minimum step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum step length of the simulation."""
        self._maxStep = 0
        """Identifies the edge that will be represented by object."""
        self._id = edgeId
        """Identifies the starting node of the edge."""
        self._fromNode = fromNode
        """Identifies the arrival node of the edge."""
        self._toNode = toNode
        """Identifies the edge length."""
        self._length = length
        """Keeps the total number of vehicles that passed through the edge over the time."""
        self._vehicleNumber = {}
        """Keeps the mean speed in m/s of vehicles that passed through the edge over the time."""
        self._meanSpeed = {}
        """Keeps the total number of vehicles stopped on the edge over the time."""
        self._haltingNumber = {}
        """Keeps the total length in meters of vehicles stopped on the edge over the time."""
        self._lengthJam = {}

        self._occupation = {}
        self._verbose = verbose

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
        """Return the identifier of the edge as an string."""
        return self._id

    @id.setter
    def id(self, edgeId):
        """Update the identifier of the edge."""
        self._id = edgeId

    @property
    def fromNode(self):
        """Return the identifier of the starting node as an string."""
        return self._fromNode

    @fromNode.setter
    def fromNode(self, fromNode):
        """Update the identifier of the starting node."""
        self._fromNode = fromNode

    @property
    def toNode(self):
        """Return the identifier of the arrival node as an string."""
        return self._toNode

    @toNode.setter
    def toNode(self, toNode):
        """Update the identifier of the arrival node."""
        self._toNode = toNode

    @property
    def length(self):
        """Return the length of the edge as an float."""
        return self._length

    @length.setter
    def length(self, length):
        """Update the length of the edge."""
        self._length = length

    @property
    def vehicleNumber(self):
        """Return the dictionary that keeps the total number of vehicles that 
        passed through the edge over the time.
        """
        return copy.deepcopy(self._vehicleNumber)

    @vehicleNumber.setter
    def vehicleNumber(self, vehicleNumberDict):
        """Overwrite the dictionary that keeps the total number of vehicles."""
        self._vehicleNumber = copy.deepcopy(vehicleNumberDict)

    @property
    def meanSpeed(self):
        """Return the dictionary that keeps the mean speed in m/s of vehicles 
        that passed through the edge over the time.
        """
        return copy.deepcopy(self._meanSpeed)

    @meanSpeed.setter
    def meanSpeed(self, meanSpeedDict):
        """Overwrite the dictionary that keeps the mean speed in m/s of vehicles."""
        self._meanSpeed = copy.deepcopy(meanSpeedDict)

    @property
    def haltingNumber(self):
        """Return the dictionary that keeps the total number of vehicles 
        stopped on the edge over the time.
        """
        return copy.deepcopy(self._haltingNumber)

    @haltingNumber.setter
    def haltingNumber(self, haltingNumberDict):
        """Overwrite the dictionary that keeps the total number of vehicles 
        stopped on the edge.
        """
        self._haltingNumber = copy.deepcopy(haltingNumberDict)

    @property
    def lengthJam(self):
        """Return the dictionary that keeps the total length in meters of 
        vehicles stopped on the edge over the time.
        """
        return copy.deepcopy(self._lengthJam)

    @property
    def occupation(self):
        """Return the dictionary that keeps the density occupation of 
        vehicles on the edge over the time.
        """
        return copy.deepcopy(self._occupation)

    @lengthJam.setter
    def lengthJam(self, lengthJamDict):
        """Overwrite the dictionary that keeps the total length in meters of 
        vehicles stopped on the edge.
        """
        self._lengthJam = copy.deepcopy(lengthJamDict)

    @occupation.setter
    def occupation(self, occupationDict):
        """Overwrite the dictionary that keeps the density occupation of 
        vehicles on the edge over the time.
        """
        self._occupation = copy.deepcopy(occupationDict)

    def getVehicleNumberOnStep(self, timeStep):
        """Return the total number of vehicles that passed through the edge 
        indicated in timeStep as an integer.
        """
        if self._vehicleNumber.has_key(timeStep):
            return self._vehicleNumber[timeStep]
        else:
            if self._verbose:
                print "Warning: Edge '" + str(self.id) + "' has no vehicles at step " + str(timeStep) + "."
            return 0

    def getMeanSpeedOnStep(self, timeStep):
        """Return the mean speed in m/s of vehicles that passed through the edge
        indicated in timeStep as an float.
        """
        if self._meanSpeed.has_key(timeStep):
            return self._meanSpeed[timeStep]
        else:
            if self._verbose:
                print "Warning: Edge '" + str(self.id) + "' has no mean speed at step " + str(timeStep) + "."
            return 0

    def getHaltingNumberOnStep(self, timeStep):
        """Return the total number of vehicles stopped at the timeStep indicated
        on the edge as an integer.
        """
        if self._haltingNumber.has_key(timeStep):
            return self._haltingNumber[timeStep]
        else:
            if self._verbose:
                print "Warning: Edge '" + str(self.id) + "' has no halting vehicles at step " + str(timeStep) + "."
            return 0

    def getLengthJamOnStep(self, timeStep):
        """Return the total length in meters of vehicles stopped at the time 
        indicated on the edge as an float.
        """
        if self._lengthJam.has_key(timeStep):
            return self._lengthJam[timeStep]
        else:
            if self._verbose:
                print "Warning: Edge '" + str(self.id) + "' has no jam length at step " + str(timeStep) + "."
            return 0

    def getoccupation(self, timeStep):
        """Return the density occupation of vehicles at the time 
        indicated on the edge as an float.
        """
        if self._occupation.has_key(timeStep):
            return self._occupation[timeStep]
        else:
            if self._verbose:
                print "Warning: Edge '" + str(self.id) + "' has no occupation at step " + str(timeStep) + "."
            return 0

    def addVehicleNumberOnStep(self, timeStep, nrVehicles):
        """Add the total number of vehicles that passed through the edge in the 
        timeStep.
        """
        self._vehicleNumber[timeStep] = nrVehicles

    def addMeanSpeedOnStep(self, timeStep, meanSpeed):
        """Add the mean speed in m/s of vehicles that passed through the edge in
        the timeStep.
        """
        self._meanSpeed[timeStep] = meanSpeed

    def addHaltingNumberOnStep(self, timeStep, nrVehicles):
        """Add the total number of vehicles stopped on the edge in the timeStep."""
        self._haltingNumber[timeStep] = nrVehicles

    def addLengthJamOnStep(self, timeStep, lengthJam):
        """Add the total length in meters of vehicles stopped on the edge in 
        the timeStep.
        """
        self._lengthJam[timeStep] = lengthJam

    def addoccupationOnStep(self, timeStep, occupation):
        """Add the density occupation of vehicles on the edge in 
        the timeStep.
        """
        self._occupation[timeStep] = occupation

    def compareEdgesAttributes(self, edgeId, fromNode, toNode, length):
        """Compare the attributes of this edge with another edge attributes and 
        return a boolean
        
        Keyword arguments:
        edgeId -- the string that identifies the edge
        fromNode -- the string that identifies the departure node
        toNode -- the string that identifies the arrival node
        length -- the float representing the size of edge

        """
        if eq(self.id,edgeId):
            if eq(self.fromNode,fromNode):
                if eq(self.toNode,toNode):
                    if eq(self.length,length):
                        return True
        return False

    def compareEdges(self, edge):
        """Compare the attributes of this edge with another edge and return a 
        boolean.

        Keyword arguments:
        edge -- the Edge object to compare

        """
        return self.compareEdgesAttributes(edge.id, edge.fromNode, edge.toNode, edge.length)

    def average(self, pattern):
        """Calculate average based on the choice of certain specified pattern,
        that is directly related to measures taken from the simulation and 
        return a float.

        Keyword arguments:
        pattern -- some constant defined for the Edge class

        """
        average = 0
        if eq(pattern,EDGE_VEHICLE_NUMBER):
            average = numpy.average(self.vehicleNumber.values())
        elif eq(pattern,EDGE_MEAN_SPEED):
            average = numpy.average(self.meanSpeed.values())
        elif eq(pattern,EDGE_HALTING_NUMBER):
            average = numpy.average(self.haltingNumber.values())
        elif eq(pattern,EDGE_JAM_LENGTH):
            average = numpy.average(self.lengthJam.values())
        elif eq(pattern,EDGE_OCCUPATION):
            average = numpy.average(self.occupation.values())
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function average()."

        return average

    def standardDeviation(self, pattern):
        """Calculate standard deviation based on the choice of certain specified
        pattern, that is directly related to measures taken from the simulation 
        and return a float.

        Keyword arguments:
        pattern -- some constant defined for the Edge class

        """
        std = 0
        if eq(pattern,EDGE_VEHICLE_NUMBER):
            std = numpy.std(self.vehicleNumber.values())
        elif eq(pattern,EDGE_MEAN_SPEED):
            std = numpy.std(self.meanSpeed.values())
        elif eq(pattern,EDGE_HALTING_NUMBER):
            std = numpy.std(self.haltingNumber.values())
        elif eq(pattern,EDGE_JAM_LENGTH):
            std = numpy.std(self.lengthJam.values())
        elif eq(pattern,EDGE_OCCUPATION):
            std = numpy.std(self.occupation.values())
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function standardDeviation()."

        return std

    def toString(self, separator=' '):
        """Return the string that represent the Edge object.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        data = []
        data.append('#id = ' + self.id + ' fromNode = ' + self.fromNode + ' toNode = ' + self.toNode + ' length = ' + self.length + '\n')
        data.append('#Time Step'+separator+'Vehicle Number'+separator+'Mean Speed(m/s)'+separator+'Halting Vehicles'+separator+'Halting Length(m)\n')
        
        if (-1 == self.minStep == self.maxStep):
            interval = self.vehicleNumber.keys()
        else:
            interval = range(self.minStep, self.maxStep)

        for timeStep in interval:
            data.append('{0}'.format(timeStep))
            data.append(separator+'{0}'.format(self.getVehicleNumberOnStep(timeStep)))
            data.append(separator+'{0:.6f}'.format(self.getMeanSpeedOnStep(timeStep)))
            data.append(separator+'{0}'.format(self.getHaltingNumberOnStep(timeStep)))
            data.append(separator+'{0:.6f}\n'.format(self.getLengthJamOnStep(timeStep)))

        return ''.join(data)
