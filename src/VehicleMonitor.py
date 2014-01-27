#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy
from operator import eq, ge, gt, attrgetter
from Constants import *
from HelpFunctions import formatListOutput

class VehicleMonitor(object):
    """Class responsible for handling a set of vehicles, and allowing selections
    about the same.
    """

    def __init__(self):
        """Keeps every necessary vehicle used in the simulation."""
        self._vehiclesDict = {}
        """Keeps for each case possible, the lists of string identifiers of 
        vehicles that must be in the simulation output.
        """
        self._vehiclesIdOutputDict = {}
        """Keeps every vehicle id that have arrived in the simulation."""
        self._vehiclesIdArrived = set()
        """Keeps the minimum step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum step length of the simulation."""
        self._maxStep = 0
        """Keeps the actual limit step length of the simulation."""
        self._steps = 0

    @property
    def vehicles(self):
        """Return the dictionary that keeps the vehicles."""
        return copy.deepcopy(self._vehiclesDict)

    @vehicles.setter
    def vehicles(self, vehicles):
        """Overwrite the dictionary that keeps the vehicles."""
        self._vehiclesDict = copy.deepcopy(vehicles)

    @property
    def vehiclesIdOutput(self):
        """Return the dictionary that keeps the vehicles identifiers string 
        lists to output.
        """
        return copy.deepcopy(self._vehiclesIdOutputDict)

    @vehiclesIdOutput.setter
    def vehiclesIdOutput(self, vehiclesIdOutputDict):
        """Overwrite the dictionary that keeps the vehicles identifiers 
        string lists to output.
        """
        self._vehiclesIdOutputDict = copy.deepcopy(vehiclesIdOutputDict)

    @property
    def vehiclesIdArrived(self):
        """Return the set of strings that keeps the arrived vehicles identifiers."""
        return copy.deepcopy(self._vehiclesIdArrived)

    @vehiclesIdArrived.setter
    def vehiclesIdArrived(self, vehiclesIdArrived):
        """Overwrite the set that keeps the arrived vehicles id."""
        self._vehiclesIdArrived = copy.deepcopy(vehiclesIdArrived)

    @property
    def minStep(self):
        """Return an integer representing the minimum step length of the 
        simulation.
        """
        return self._minStep

    @minStep.setter
    def minStep(self, minStep):
        """Overwrite the minimum step length of the simulation."""
        self._minStep = minStep

    @property
    def maxStep(self):
        """Return an integer representing the maximum step length of the 
        simulation.
        """
        return self._maxStep

    @maxStep.setter
    def maxStep(self, maxStep):
        """Overwrite the maximum step length of the simulation."""
        self._maxStep = maxStep

    def addVehicle(self, vehicle, key=None):
        """Add one vehicle object in the key position of the monitor. If key is 
        None or absent, then adds in the next free position.

        Keyword arguments:
        vehicle -- an Vehicle object
        key -- an integer that identifies the position in a dictionary

        """
        if eq(key,None) or (not self._vehiclesDict.has_key(key)):
            key = self.getSize()

        self._vehiclesDict[key] = copy.deepcopy(vehicle)

    def addVehiclesIdOutput(self, vehicleIdList, key):
        """Add an list of strings representing vehicles identifiers in the 
        dictionary, in the position that has been defined by a name constant.

        Keyword arguments:
        vehicleIdList -- an list of strings representing vehicles identifiers
        key -- an name constant related to Vehicle class

        """
        if self._vehiclesIdOutputDict.has_key(key):
            dif = list(set(vehicleIdList).difference(set(self._vehiclesIdOutputDict[key])))
            self._vehiclesIdOutputDict[key].extend(dif)
        else:
            self._vehiclesIdOutputDict[key] = copy.deepcopy(vehicleIdList)

    def vehiclesIdOutputKeys(self):
        """Return a list of strings representing vehicles identifiers of the 
        dictionary output.
        """
        return self._vehiclesIdOutputDict.keys()

    def addVehicleIdArrived(self, vehicleId):
        """Add a id of the vehicle that have arrived.

        Keyword arguments:
        vehicleId -- an string that identifies an vehicle object

        """
        self._vehiclesIdArrived.add(vehicleId)

    def updateVehiclesIdArrived(self, vehicleIdList):
        """Add a list of vehicles id that have arrived.

        Keyword arguments:
        vehicleIdList -- an list of strings representing vehicles identifiers

        """
        self._vehiclesIdArrived.update(vehicleIdList)

    def getSize(self):
        """Return an integer representing the number of vehicles in the monitor."""
        return len(self._vehiclesDict)

    def removeVehicleByKey(self, key):
        """Remove the vehicle object in the key position and return a boolean.

        Keyword arguments:
        key -- an integer that identifies the position in a dictionary

        """
        if self._vehiclesDict.has_key(key):
            try:
                del self._vehiclesDict[key]        
                return True
            except KeyError:
                print "Failed to remove key '"+str(key)+"' for the list of vehicles."
                return False
        else:
            return False

    def removeVehicleById(self, vehicleId):
        """Remove the vehicle object that matching the string identifier and 
        return a boolean.

        Keyword arguments:
        vehicleId -- an string that identifies an vehicle object

        """
        for key,vehicle in self._vehiclesDict.iteritems():
            if eq(vehicle.id,vehicleId):
                try:
                    del self._vehiclesDict[key]
                    return True
                except KeyError:
                    print "Failed to remove vehicle '"+str(vehicleId)+"' from key '"+str(key)+"' for the list of vehicles."
                    return False
        # If the key is inexistent
        return False

    def getVehicleByKey(self, key):
        """Return the vehicle object in the key position. If the key is invalid,
        returns None.

        Keyword arguments:
        key -- an integer that identifies the position in a dictionary

        """
        if self._vehiclesDict.has_key(key):
            return copy.deepcopy(self._vehiclesDict.get(key))
        else:
            return None

    def hasVehicleById(self, vehicleId):
        """Return True if has an vehicle object that matching the identifier. 
        Return False otherwise.

        Keyword arguments:
        vehicleId -- an string that identifies an vehicle object

        """
        for vehicle in self._vehiclesDict.values():
            if eq(vehicle.id,vehicleId):
                return True

        # If the vehicleId is inexistent
        return False

    def getVehicleById(self, vehicleId):
        """Return the vehicle object that matching the identifier. If the key is
        invalid, returns None.

        Keyword arguments:
        vehicleId -- an string that identifies an vehicle object

        """
        for vehicle in self._vehiclesDict.values():
            if eq(vehicle.id,vehicleId):
                return copy.deepcopy(vehicle)

        # If the key is inexistent
        return None

    def getVehicleListByKey(self, keyList):
        """Return a dictionary containing the vehicle objects that matching the 
        key list. If all the keys are invalid, returns an empty dictionary.

        Keyword arguments:
        keyList -- an list of integers that identifies positions in a dictionary

        """
        vehicles = {}
        if gt(len(keyList),0):
            for key in keyList:
                vehicles[len(vehicles)] = self.getVehicleByKey(key)
        return copy.deepcopy(vehicles)

    def getVehicleListById(self, vehicleIdList):
        """Return a dictionary containing the vehicle objects that matching the 
        id list. If all the id's are invalid, returns an empty dictionary.

        Keyword arguments:
        vehicleIdList -- an list of strings representing vehicles identifiers

        """
        vehicles = {}
        for vehicleId in vehicleIdList:
            vehicles[len(vehicles)] = self.getVehicleById(vehicleId)
        return copy.deepcopy(vehicles)

    def getVehiclesIdList(self):
        """Return a list of strings representing the vehicle identifier to 
        output.
        """
        return [vehicle.id for vehicle in self.vehicles.values()]

    def getVehiclesIdListOutput(self, key):
        """Return the list of strings representing the vehicle identifiers to 
        output at the key position. If the key is invalid, returns a empty list.

        Keyword arguments:
        key -- an name constant related to Vehicle class

        """
        if self._vehiclesIdOutputDict.has_key(key):
            return copy.deepcopy(self._vehiclesIdOutputDict.get(key))
        else:
            return []

    #TODO: need a revision, not used
    def getVehiclesAmount(self, amount, orderBy, invert=False):
        """Return a dictionary that contains 'amount' of Vehicle objects which 
        are at the beginning of the dictionary of vehicles, based on average of 
        the measure represented by 'orderBy'.

        If 'amount' is bigger than the number of vehicles in the dictionary, 
        returns the entire dictionary.

        Keyword arguments:
        amount -- an integer that quantifies the call
        orderBy -- an constant related to Vehicles
        invert -- swap the begin or end of the output

        """
        vehicles = {}
        if ge(amount,0):
            if ge(amount, self.getSize()):
                return self.vehicles

            #keyOrder = lambda vehicle: sum(vehicle._id)/len(vehicle._id)
            #keyOrder = "_id" sum(vehicle._id)/len(vehicle._id)
            keyOrder = attrgetter("_id")
            #TODO: Arrumar isso
            if(eq(orderBy,VEHICLE_SPEED)):
                keyOrder = lambda vehicle: vehicle.average(VEHICLE_SPEED)

            key = 0
            for vehicle in (sorted(self.vehicles.values(), key=keyOrder, reverse=invert)):
                if ge(key, amount):
                    break
                vehicles[len(vehicles)] = vehicle
                key += 1

        return copy.deepcopy(vehicles)

    def updateVehicle(self, timeStep, vehicleId, speed, routeId, routeList, edgeId, edgeLength):
        """Update the vehicles with the data extracted for simulation for every 
        step time.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation 
        vehicleId -- an string that identifies an vehicle object 
        speed -- an float that represent the speed of the vehicle
        routeId -- an string that identifies an route
        routeList -- an list of strings that represent the path traveled by the 
            vehicle
        edgeId -- an string that identifies an edge object
        edgeLength -- an float that represent the size of the edge

        """
        self._steps += 1
        for key, vehicle in self._vehiclesDict.items():
            if eq(vehicle.id, vehicleId):
                # Updates the number of vehicles in the edge in this time step.
                self._vehiclesDict[key].addSpeedOnStep(timeStep, speed)
                self._vehiclesDict[key].updateRoutes(timeStep, routeId, routeList)
                self._vehiclesDict[key].updateDistance(timeStep, edgeId, edgeLength)

    def updateArrivedVehicle(self, timeStep, vehicleId):
        """Update the arrived vehicles with the data extracted for simulation at
        arrival time.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation 
        vehicleId -- an string that identifies an vehicle object 

        """
        for key, vehicle in self._vehiclesDict.items():
            if eq(vehicle.id, vehicleId):
                self._vehiclesDict[key].arrival = timeStep
                self.addVehicleIdArrived(vehicleId)
    
    def update(self, timeStep):
        """Make a correction in the arrival time for the vehicles that not 
        arrived at end of the simulation.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation 

        """
        for vehiclesIdList in self.vehiclesIdOutput.values():
            vehiclesIdSet = set(vehiclesIdList)
            vehiclesNotArrivedSet = vehiclesIdSet.difference(self.vehiclesIdArrived)
            for vehicleId in vehiclesNotArrivedSet:
                self.updateArrivedVehicle(timeStep, vehicleId)

    def toString(self, pattern, separator=' '):
        """Return a string that contains data referring to the Vehicle objects from
        simulation.

        Keyword arguments:
        pattern -- some constant defined for the Edge class
        separator -- the constant defined for string format

        """
        saida = []
        header = []
        values = []
        routes = []

        # Adds the header
        if eq(pattern,VEHICLE_DISTANCE) or eq(pattern,VEHICLE_TIME) or eq(pattern,VEHICLE_SPEED) or eq(pattern,VEHICLE_ROUTE):
            if self._vehiclesIdOutputDict.has_key(pattern):
                for vehicle in self._vehiclesDict.values():
                    if vehicle.id in self._vehiclesIdOutputDict.get(pattern):
                        header.append(vehicle.id)

        # Adds the data for each vehicle.
        if self._vehiclesIdOutputDict.has_key(pattern):
            for vehicle in self._vehiclesDict.values():
                if vehicle.id in self._vehiclesIdOutputDict.get(pattern):
                    if eq(pattern,VEHICLE_DISTANCE):
                        values.append('{0:.2f}'.format(vehicle.getTraveledDistance()))
                    elif eq(pattern,VEHICLE_TIME):
                        values.append('{0}'.format(vehicle.getTraveledTime()))
                    elif eq(pattern,VEHICLE_SPEED):
                        values.append('{0:.6f}'.format(vehicle.getMeanSpeed()))
                    elif eq(pattern,VEHICLE_ROUTE):
                        # Creates a list of the vehicle last route
                        routeId, routeList = vehicle.getCurrentRoute()
                        values.append(formatListOutput(routeList))
                        # Creates a list of the edges that the vehicle passed
                        values2 = []
                        keyOrder = lambda (edgeId, distance): distance
                        for edgeId in sorted(vehicle.distance.values(), key=keyOrder):
                            if not edgeId[0].startswith('-'):
                                values2.append(edgeId[0])
                        routes.append(formatListOutput(values2))
        if eq(pattern,VEHICLE_ROUTE):
            saida.append('# Observation: Second line is the last route of the vehicle. Third line is the edges visited.')
        else:
            saida.append('# Observation: Zero value is for vehicles that have not departed.')

        saida.append('#'+separator.join(header))
        saida.append(separator.join(values))
        saida.append(separator.join(routes))
        return '\n'.join(saida)

    def toStringEvaluate(self,separator=' '):
        """Return a string that contains data referring the average of the 
        vehicles from simulation.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        saida = ['# Observation: Zero value is for vehicles that have not departed.']
        header = ['#Vehicles']; avgS = ['VehicleSpeed(avg)(m/s)']; stdS = ['VehicleSpeed(stdDev)(m/s)'];
        # Adds the data
        for vehicle in self._vehiclesDict.values():
            header.append(vehicle.id)
            avgS.append('{0:.6f}'.format(vehicle.average(VEHICLE_SPEED)))
            stdS.append('{0:.6f}'.format(vehicle.standardDeviation(VEHICLE_SPEED)))
        saida.append(separator.join(header))
        saida.append(separator.join(avgS))
        saida.append(separator.join(stdS))

        return '\n'.join(saida)

    def toStringEvaluateReverse(self,separator=' '):
        """Return a string that contains data referring the average of the 
        vehicles from simulation.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        saida = []
        saida.append('#Vehicles'+separator+'VehicleSpeed(avg)(m/s)'+separator+'VehicleSpeed(stdDev)(m/s)')
        # Adds the data
        for vehicle in self._vehiclesDict.values():
            saida.append(vehicle.id)
            saida.append(separator+'{0:.6f}'.format(vehicle.average(VEHICLE_SPEED)))
            saida.append(separator+'{0:.6f}'.format(vehicle.standardDeviation(VEHICLE_SPEED)))
            saida.append('\n')
        return ''.join(saida)

    def debug(self):
        """An standardized output for verification."""
        for veh in self.vehicles.values():
            print veh.toString()
