#!/usr/bin/env python
#-*- coding: utf-8 -*-

from operator import eq
import numpy
import copy
from Constants import *
from HelpFunctions import *

class Vehicle(object):
    """Class responsible for handling one Vehicle object."""

    def __init__(self, vehicleId):
        """Keeps the minimum time step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum time step length of the simulation."""
        self._maxStep = 0
        """Identifies the vehicle that will be represented by object."""
        self._id = vehicleId
        """Keeps the speed in m/s of the vehicle at each simulation step."""
        self._speed = {}
        """Keeps the time step of the vehicle departure."""
        self._departure = 0
        """Keeps the time step of the vehicle arrival."""
        self._arrival = 0
        """Keeps the route of the vehicle on the simulation."""
        self._route = {}
        """Keeps the accumulated travel distance by the vehicle at each 
        simulation step.
        """
        self._distance = {}

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
        """Return the identifier of the vehicle as an string."""
        return self._id

    @id.setter
    def id(self, vehicleId):
        """Update the identifier of the vehicle."""
        self._id = vehicleId

    @property
    def speed(self):
        """Return the dictionary of integers that keeps the speed in m/s of the 
        vehicle.
        """
        return copy.deepcopy(self._speed)

    @speed.setter
    def speed(self, speedDict):
        """Overwrite the dictionary that keeps the speed in m/s of vehicles."""
        self._speed = copy.deepcopy(speedDict)

    @property
    def departure(self):
        """Return the departure time step of the vehicle as an integer."""
        return self._departure

    @departure.setter
    def departure(self, departureTime):
        """Update the departure time step of the vehicle."""
        self._departure = departureTime

    @property
    def arrival(self):
        """Return the arrival time step of the vehicle as an integer."""
        return self._arrival

    @arrival.setter
    def arrival(self, arrivalTime):
        """Update the arrival time step of the vehicle."""
        self._arrival = arrivalTime

    @property
    def route(self):
        """Return a copy of the route dictionary of the vehicle."""
        return copy.deepcopy(self._route)

    @route.setter
    def route(self, routeDict):
        """Overwrite the route dictionary of the vehicle."""
        self._route = copy.deepcopy(routeDict)

    @property
    def distance(self):
        """Return the dictionary of float distance traveled by the vehicle."""
        return copy.deepcopy(self._distance)

    @distance.setter
    def distance(self, distanceDict):
        """Overwrite the dictionary of distance traveled by the vehicle."""
        self._distance = copy.deepcopy(distanceDict)

    def hasDistanceOnStep(self, timeStep):
        """Verify if exist a distance traveled by the vehicle in the simulation 
        step and return a boolean.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation

        """
        return self._distance.has_key(timeStep)

    def addDistance(self, timeStep, edgeId, distance):
        """Add the initial distance traveled by the vehicle.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        edgeId -- an string identifier for the edge
        distance -- an float representing traveled distance

        """
        self._distance[timeStep] = (edgeId, distance)

    def updateDistance(self, timeStep, edgeId, distance):
        """Update the distance traveled by the vehicle.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        edgeId -- an string identifier for the edge
        distance -- an float representing traveled distance

        """
        edgeIdC, distanceC = self.getCurrentEdge()
        if not eq(edgeIdC, edgeId):
            self.addDistance(timeStep, edgeId, distanceC+distance)

    def getCurrentEdge(self):
        """Return an tuple representing the current edge and distance traversed 
        by the vehicle.
        """
        keys = self._distance.keys()
        if keys:
            return self._distance[max(keys)]
        else:
            return ('-',0)

    def getTraveledDistance(self):
        """Return an float representing the total distance traveled by the 
        vehicle.
        """
        edgeId, distance = self.getCurrentEdge()
        return distance

    def getTraveledTime(self):
        """Return a float representing the total time traveled by the vehicle."""
        return abs(self.arrival - self.departure)

    def addRouteOnStep(self, timeStep, routeId, routeList):
        """Add to the dictionary of routes the current route of the vehicle.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        routeId -- an string identifier for the route
        routeList -- an list of strings representing the path to travel

        """
        self._route[timeStep] = (routeId, routeList)

    def hasRouteOnStep(self, timeStep):
        """Return True if the dictionary has routes at timeStep, False in 
        otherwise.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation

        """
        return self._route.has_key(timeStep)

    def getRouteOnStep(self, timeStep):
        """Return the route tuple at indicated timeStep.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation

        """
        if self.hasRouteOnStep(timeStep):
            return self._route[timeStep]
        else:   # default case empty values
            return ('-','-')

    def getCurrentRoute(self):
        """Return an tuple representing the current route."""
        keys = self._route.keys()
        if keys:
            return self._route[max(keys)]
        else:
            return ('-','-')

    def updateRoutes(self, timeStep, routeId, routeList):
        """Update the dictionary that keeps the routes of the vehicle.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        routeId -- an string identifier for the route
        routeList -- an list of strings representing the path to travel

        """
        routeIdC, routeListC = self.getCurrentRoute()
        if not eq(routeIdC, routeId):
            self.addRouteOnStep(timeStep, routeId, routeList)

    def removeRouteById(self, routeId):
        """Remove the route that has been identified and return a boolean.

        Keyword arguments:
        routeId -- an string identifier for the route

        """
        for key, value in self._route.items():
            if eq(routeId, value[0]):
                del self._route[key]
                return True

        return False

    def removeRouteByKey(self, key):
        """Remove the route at the key position and return a boolean.

        Keyword arguments:
        key -- an integer that identifies the position in a dictionary

        """
        if self._route.has_key(key):
            del self._route[key]
            return True

        return False

    def addSpeedOnStep(self, timeStep, speed):
        """Add the speed in m/s of the vehicle in the timeStep.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        speed -- an float that represents the speed of the vehicle

        """
        self._speed[timeStep] = speed

    def hasSpeedOnStep(self, timeStep):
        """Returns True if the vehicle has speed in indicated timeStep, False in
        otherwise.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation

        """
        return self._speed.has_key(timeStep)

    def getSpeedOnStep(self, timeStep):
        """Return a float representing the speed in m/s of the vehicle indicated
        in timeStep.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation

        """
        if self.hasSpeedOnStep(timeStep):
            return self._speed[timeStep]
        else:   # default case zero value
            return 0

    def getMeanSpeed(self):
        """Return a float representing the mean speed of the vehicle based in 
        the distance traveled and the time spent.
        """
        distance = self.getTraveledDistance()
        time = self.getTraveledTime()
        # escape from division by zero
        if eq(time,0):
            time = 1
        return distance / time

    def compareVehiclesAttributes(self, vehicleId):
        """Compare the attributes of this vehicle with another vehicle 
        attributes and return a boolean.

        Keyword arguments:
        vehicleId -- an string that identifies the Vehicle object

        """
        if eq(self.id,vehicleId):
            return True
        return False

    def compareVehicles(self, vehicle):
        """Compare the attributes of this vehicle with another vehicle and 
        return a boolean.

        Keyword arguments:
        vehicle -- an Vehicle object

        """
        return self.compareVehiclesAttributes(vehicle.id)

    def average(self, pattern):
        """Calculate average based on the choice of certain specified pattern,
        that is directly related to measures taken from the simulation and 
        return a list of float.

        Keyword arguments:
        pattern -- some constant defined for the Vehicle class

        """
        average = 0
        if eq(pattern,VEHICLE_SPEED):
            values = self.speed.values()
            if values:
                average = numpy.average(values)
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function average()."

        return average

    def standardDeviation(self, pattern):
        """Calculate standard deviation based on the choice of certain specified
        pattern, that is directly related to measures taken from the simulation 
        and return a list of float.

        Keyword arguments:
        pattern -- some constant defined for the Vehicle class

        """
        std = 0
        if eq(pattern,VEHICLE_SPEED):
            values = self.speed.values()
            if values:
                std = numpy.std(values)
        else:
            print "Warning: pattern "+str(pattern)+" not recognized at function standardDeviation()."

        return std

    def toString(self, separator=' '):
        """Return the string that represent the vehicle object.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        data = []
        data.append('#Id='+self.id+separator+'Departure='+str(self.departure)+separator+'Arrival='+str(self.arrival)+'\n')
        data.append('#Distance={0:.2f}'.format(self.getTraveledDistance())+separator+'Time={0}'.format(self.getTraveledTime())+separator+'MeanSpeed={0:.6f}'.format(self.getMeanSpeed())+'\n')
        data.append('#LastRoute'+separator+'Path\n')
        routeId, routeList = self.getCurrentRoute()
        data.append(formatListOutput(routeList))
        path = []
        keyOrder = lambda (edgeId, distance): distance
        for edgeId in sorted(self.distance.values(), key=keyOrder):
            if not edgeId[0].startswith('-'):
                path.append(edgeId[0])
        data.append(separator+formatListOutput(path))

        data.append('\n')
        data.append('#Time Step'+separator+'Speed\n')

        if (-1 == self.minStep == self.maxStep):
            interval = self.speed.keys()
        else:
            interval = range(self.minStep, self.maxStep)

        for timeStep in interval:
            data.append('{0}'.format(timeStep))
            data.append(separator+'{0:.6f}'.format(self.getSpeedOnStep(timeStep)))
            data.append('\n')

        return ''.join(data)
