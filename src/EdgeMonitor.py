#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy
from operator import eq, ge, gt, attrgetter
from Constants import *

class EdgeMonitor(object):
    """Class responsible for handling a set of edges, and allowing selections 
    about the same.
    """

    def __init__(self):
        """Keeps every necessary edge used in the simulation."""
        self._edgesDict = {}
        """Keeps  for each case possible, the lists of ids of edges that must be in the simulation output."""
        self._edgesIdOutputDict = {}
        """Keeps the minimum step length of the simulation."""
        self._minStep = 0
        """Keeps the maximum step length of the simulation."""
        self._maxStep = 0
        """Keeps the actual limit step length of the simulation."""
        self._steps = 0
        self._timeStep = 0

    @property
    def edges(self):
        """Return the dictionary that keeps the edges."""
        return copy.deepcopy(self._edgesDict)

    @edges.setter
    def edges(self, edges):
        """Overwrite the dictionary that keeps the edges."""
        self._edgesDict = copy.deepcopy(edges)

    @property
    def edgesIdOutput(self):
        """Return the dictionary that keeps the edges id lists to output."""
        return copy.deepcopy(self._edgesIdOutputDict)

    @edgesIdOutput.setter
    def edgesIdOutput(self, edgesIdDict):
        """Overwrite the dictionary that keeps the edges id lists to output."""
        self._edgesIdOutputDict = copy.deepcopy(edgesIdDict)

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

    def addEdge(self, edge, key=None):
        """Add one Edge object in the key position of the monitor. If key
        is None or absent, then adds in the next free position.

        Keyword arguments:
        edge -- an Edge object
        key -- an integer that identifies the position in a dictionary

        """
        if eq(key,None) or (not self._edgesDict.has_key(key)):
            key = self.getSize()

        self._edgesDict[key] = copy.deepcopy(edge)

    def addEdgesIdOutput(self, edgeIdList, key):
        """Add a list of edges id in the dictionary, in the position that has 
        been defined by a name constant.

        Keyword arguments:
        edgeIdList -- a list of strings
        key -- an constant related to Edge class

        """
        self._edgesIdOutputDict[key] = copy.deepcopy(edgeIdList)

    def edgesIdOutputKeys(self):
        """Return a list of strings represented by edges id of the dictionary 
        output.
        """
        return self._edgesIdOutputDict.keys()

    def getSize(self):
        """Return the number of edges in the monitor as a integer."""
        return len(self._edgesDict)

    def removeEdgeByKey(self, key):
        """Remove the edge object in the key position and returns False if the 
        key is absent, True in success.

        Keyword arguments:
        key -- an integer that identifies the position in a dictionary

        """
        if self._edgesDict.has_key(key):
            try:
                del self._edgesDict[key]
                return True
            except KeyError:
                print "Failed to remove key '"+str(key)+"' for the list of edges."
                return False
        else:
            return False

    def removeEdgeById(self, edgeId):
        """Remove the edge object that matching the identifier and returns False
        if the identifier is absent, True in success.

        Keyword arguments:
        edgeId -- an string that identifies an Edge object

        """
        for key,edge in self._edgesDict.iteritems():
            if eq(edge.id,edgeId):
                try:
                    del self._edgesDict[key]
                    return True
                except KeyError:
                    print "Failed to remove edge '"+str(edgeId)+"' from key '"+str(key)+"' for the list of edges."
                    return False
        # If the key is inexistent
        return False

    def getEdgeByKey(self, key):
        """Return the edge object in the key position. If the key is invalid, 
        returns None.

        Keyword arguments:
        key -- an integer that identifies the position in a dictionary

        """
        if self._edgesDict.has_key(key):
            return copy.deepcopy(self._edgesDict.get(key))
        else:
            return None

    def getEdgeById(self, edgeId):
        """Return the edge object that matching the identifier. If the 
        identifier is invalid, returns None.

        Keyword arguments:
        edgeId -- an string that identifies an Edge object

        """
        for edge in self._edgesDict.values():
            if eq(edge.id,edgeId):
                return copy.deepcopy(edge)

        # If the identifier is inexistent
        return None

    def getEdgeListByKey(self, keyList):
        """Return a dictionary containing the Edge objects that matching the 
        key list. If all the keys are invalid, returns an empty dictionary.

        Keyword arguments:
        keyList -- a list of integers that identifies the position in a dictionary

        """
        edges = {}
        if gt(len(keyList),0):
            for key in keyList:
                edges[len(edges)] = self.getEdgeByKey(key)
        return copy.deepcopy(edges)

    def getEdgeListById(self, edgeIdList):
        """Return a dictionary containing the edge objects that matching the 
        identifier list. If all the identifiers are invalid, returns an empty 
        dictionary.

        Keyword arguments:
        edgeIdList -- a list of strings that identifies the Edge objects

        """
        edges = {}
        for edgeId in edgeIdList:
            edges[len(edges)] = self.getEdgeById(edgeId)
        return copy.deepcopy(edges)

    #TODO: need a revision, and not used
    def getEdgesAmount(self, amount, orderBy, invert=False):
        """Return a dictionary that contains 'amount' of Edge objects which are 
        at the beginning of the dictionary of edges, based on average of the 
        measure represented by 'orderBy'.

        If 'amount' is bigger than the number of edges in the dictionary, 
        returns the entire dictionary.

        Keyword arguments:
        amount -- an integer that quantifies the call
        orderBy -- an constant related to Edges
        invert -- swap the begin or end of the output

        """
        edges = {}
        if ge(amount,0):
            if ge(amount, self.getSize()):
                return self.edges

            #keyOrder = lambda edge: sum(edge._id)/len(edge._id)
            #keyOrder = "_id" sum(edge._id)/len(edge._id)
            keyOrder = attrgetter("_id")
            if eq(orderBy,EDGE_VEHICLE_NUMBER):
                keyOrder = lambda edge: edge.average(EDGE_VEHICLE_NUMBER)
            elif eq(orderBy,EDGE_MEAN_SPEED):
                keyOrder = lambda edge: edge.average(EDGE_MEAN_SPEED)
            elif eq(orderBy,EDGE_HALTING_NUMBER):
                keyOrder = lambda edge: edge.average(EDGE_HALTING_NUMBER)
            elif eq(orderBy,EDGE_JAM_LENGTH):
                keyOrder = lambda edge: edge.average(EDGE_JAM_LENGTH)
            elif eq(orderBy,EDGE_OCCUPATION):
                keyOrder = lambda edge: edge.average(EDGE_OCCUPATION)

            #for qtd in range(quantity):
                #for edge in (sorted(self._vetorEdges.values(), key=attrgetter(keyOrder))):
            key = 0
            for edge in sorted(self.edges.values(), key=keyOrder, reverse=invert):
                if ge(key, amount):
                    break
                edges[len(edges)] = edge
                key += 1

        return copy.deepcopy(edges)

    def updateEdge(self, timeStep, edgeId, vehicleNumber, meanSpeed, haltingNumber, lengthJam, occupation):
        """Update the identified edge object with the data extracted from 
        simulation for every time step.

        Keyword arguments:
        timeStep -- an integer that represents the step of simulation
        edgeId -- an string that identifies an Edge object 
        vehicleNumber -- an integer that represents the number of vehicles 
            that passed through the edge
        meanSpeed -- an float that represents the average speed of vehicles 
            that passed through the edge
        haltingNumber -- an integer that represents the number of vehicles 
            that stopped on the edge
        lengthJam -- an float that represents the length of traffic jam on the 
            edge

        """
        self._steps += 1
        self._timeStep = timeStep
        for key,edge in self._edgesDict.items():
            if eq(edge.id,edgeId):
                # Updates the number of vehicles in the edge in this time step.
                self._edgesDict[key].addVehicleNumberOnStep(timeStep, vehicleNumber)
                # Updates the mean speed of vehicles in the edge in this time step.
                self._edgesDict[key].addMeanSpeedOnStep(timeStep, meanSpeed)
                # Updates the number of vehicles stopped in the edge in this time step.
                self._edgesDict[key].addHaltingNumberOnStep(timeStep, haltingNumber)
                # Updates the length of vehicles stopped in the edge in this time step.
                self._edgesDict[key].addLengthJamOnStep(timeStep, lengthJam)
                self._edgesDict[key].addoccupationOnStep(timeStep, occupation)

    def toString(self, pattern, separator=' '):
        """Return a string that contains data referring to the edge objects from
        simulation.

        Keyword arguments:
        pattern -- some constant defined for the Edge class
        separator -- the constant defined for string format

        """
        saida = ['#TimeStep']

        # Adds the header
        for edge in self._edgesDict.values():
            if eq(pattern,EDGE_VEHICLE_NUMBER):
                if self._edgesIdOutputDict.has_key(EDGE_VEHICLE_NUMBER):
                    if edge.id in self._edgesIdOutputDict.get(EDGE_VEHICLE_NUMBER):
                        saida.append(separator+edge.id)
            elif eq(pattern,EDGE_MEAN_SPEED):
                if self._edgesIdOutputDict.has_key(EDGE_MEAN_SPEED):
                    if edge.id in self._edgesIdOutputDict.get(EDGE_MEAN_SPEED):
                        saida.append(separator+edge.id)
            elif eq(pattern,EDGE_HALTING_NUMBER):
                if self._edgesIdOutputDict.has_key(EDGE_HALTING_NUMBER):
                    if edge.id in self._edgesIdOutputDict.get(EDGE_HALTING_NUMBER):
                        saida.append(separator+edge.id)
            elif eq(pattern,EDGE_JAM_LENGTH):
                if self._edgesIdOutputDict.has_key(EDGE_JAM_LENGTH):
                    if edge.id in self._edgesIdOutputDict.get(EDGE_JAM_LENGTH):
                        saida.append(separator+edge.id)
            elif eq(pattern,EDGE_OCCUPATION):
                if self._edgesIdOutputDict.has_key(EDGE_OCCUPATION):
                    if edge.id in self._edgesIdOutputDict.get(EDGE_OCCUPATION):
                        saida.append(separator+edge.id)
        saida.append('\n')

        # Adds the data for each time step.
        if (-1 == self.minStep == self.maxStep):
            interval = range(0, self._timeStep)
        else:
            interval = range(self.minStep, self.maxStep)

        for timeStep in interval:
            saida.append('{0}'.format(timeStep))

            for edge in self._edgesDict.values():
                if eq(pattern,EDGE_VEHICLE_NUMBER):
                    if self._edgesIdOutputDict.has_key(EDGE_VEHICLE_NUMBER):
                        if edge.id in self._edgesIdOutputDict.get(EDGE_VEHICLE_NUMBER):
                            saida.append(separator+'{0}'.format(edge.getVehicleNumberOnStep(timeStep)))
                elif eq(pattern,EDGE_MEAN_SPEED):
                    if self._edgesIdOutputDict.has_key(EDGE_MEAN_SPEED):
                        if edge.id in self._edgesIdOutputDict.get(EDGE_MEAN_SPEED):
                            saida.append(separator+'{0:.6f}'.format(edge.getMeanSpeedOnStep(timeStep)))
                elif eq(pattern,EDGE_HALTING_NUMBER):
                    if self._edgesIdOutputDict.has_key(EDGE_HALTING_NUMBER):
                        if edge.id in self._edgesIdOutputDict.get(EDGE_HALTING_NUMBER):
                            saida.append(separator+'{0}'.format(edge.getHaltingNumberOnStep(timeStep)))
                elif eq(pattern,EDGE_JAM_LENGTH):
                    if self._edgesIdOutputDict.has_key(EDGE_JAM_LENGTH):
                        if edge.id in self._edgesIdOutputDict.get(EDGE_JAM_LENGTH):
                            saida.append(separator+'{0:.6f}'.format(edge.getLengthJamOnStep(timeStep)))
                elif eq(pattern,EDGE_OCCUPATION):
                    if self._edgesIdOutputDict.has_key(EDGE_OCCUPATION):
                        if edge.id in self._edgesIdOutputDict.get(EDGE_OCCUPATION):
                            saida.append(separator+'{0:.6f}'.format(edge.getoccupation(timeStep)))

            saida.append('\n')

        return ''.join(saida)

    def toStringEvaluate(self,separator=' '):
        """Return a string that contains data referring the average of the edges
        from simulation.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        saida = []
        header = ['#Edges']; avgN = ['VehicleNumber(avg)']; stdN = ['VehicleNumber(stdDev)']; 
        avgS = ['MeanSpeed(avg)(m/s)']; stdS = ['MeanSpeed(stdDev)(m/s)']; avgH = ['HaltingVehicles(avg)']; 
        stdH = ['HaltingVehicles(stdDev)']; avgL = ['HaltingLength(avg)(m)']; stdL = ['HaltingLength(stdDev)(m)'];
        avgO = ['Occupation(avg)(m)']; stdO = ['Occupation(stdDev)(m)'];
        # Adds the data
        for edge in self._edgesDict.values():
            header.append(edge.id)
            avgN.append('{0:.6f}'.format(edge.average(EDGE_VEHICLE_NUMBER)))
            stdN.append('{0:.6f}'.format(edge.standardDeviation(EDGE_VEHICLE_NUMBER)))
            avgS.append('{0:.6f}'.format(edge.average(EDGE_MEAN_SPEED)))
            stdS.append('{0:.6f}'.format(edge.standardDeviation(EDGE_MEAN_SPEED)))
            avgH.append('{0:.6f}'.format(edge.average(EDGE_HALTING_NUMBER)))
            stdH.append('{0:.6f}'.format(edge.standardDeviation(EDGE_HALTING_NUMBER)))
            avgL.append('{0:.6f}'.format(edge.average(EDGE_JAM_LENGTH)))
            stdL.append('{0:.6f}'.format(edge.standardDeviation(EDGE_JAM_LENGTH)))
            avgO.append('{0:.6f}'.format(edge.average(EDGE_OCCUPATION)))
            stdO.append('{0:.6f}'.format(edge.standardDeviation(EDGE_OCCUPATION)))
        saida.append(separator.join(header))
        saida.append(separator.join(avgN))
        saida.append(separator.join(stdN))
        saida.append(separator.join(avgS))
        saida.append(separator.join(stdS))
        saida.append(separator.join(avgH))
        saida.append(separator.join(stdH))
        saida.append(separator.join(avgL))
        saida.append(separator.join(stdL))
        saida.append(separator.join(avgO))
        saida.append(separator.join(stdO))

        return '\n'.join(saida)

    def toStringEvaluateReverse(self,separator=' '):
        """Return a string that contains data referring the average of the edges
        from simulation.

        Keyword arguments:
        separator -- the constant defined for string format

        """
        saida = []
        saida.append('#Edges'+separator+'VehicleNumber(avg)'+separator+'VehicleNumber(stdDev)'+separator+'MeanSpeed(avg)(m/s)'+separator+'MeanSpeed(stdDev)(m/s)'+separator+'HaltingVehicles(avg)'+separator+'HaltingVehicles(stdDev)'+separator+'HaltingLength(avg)(m)'+separator+'HaltingLength(stdDev)(m)'+separator+'Occupation(avg)'+separator+'Occupation(stdDev)\n')
        # Adds the data
        for edge in self._edgesDict.values():
            saida.append(edge.id)
            saida.append(separator+'{0:.6f}'.format(edge.average(EDGE_VEHICLE_NUMBER)))
            saida.append(separator+'{0:.6f}'.format(edge.standardDeviation(EDGE_VEHICLE_NUMBER)))
            saida.append(separator+'{0:.6f}'.format(edge.average(EDGE_MEAN_SPEED)))
            saida.append(separator+'{0:.6f}'.format(edge.standardDeviation(EDGE_MEAN_SPEED)))
            saida.append(separator+'{0:.6f}'.format(edge.average(EDGE_HALTING_NUMBER)))
            saida.append(separator+'{0:.6f}'.format(edge.standardDeviation(EDGE_HALTING_NUMBER)))
            saida.append(separator+'{0:.6f}'.format(edge.average(EDGE_JAM_LENGTH)))
            saida.append(separator+'{0:.6f}'.format(edge.standardDeviation(EDGE_JAM_LENGTH)))
            saida.append(separator+'{0:.6f}'.format(edge.average(EDGE_OCCUPATION)))
            saida.append(separator+'{0:.6f}'.format(edge.standardDeviation(EDGE_OCCUPATION)))
            saida.append('\n')
        return ''.join(saida)