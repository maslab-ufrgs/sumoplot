#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Default libraries
import os 
import sys
from random import random
from operator import ge, le, eq, gt
from copy import copy

# Development libraries
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), 'src'))
from Edge import Edge
from EdgeMonitor import EdgeMonitor
from Vehicle import Vehicle
from VehicleMonitor import VehicleMonitor
from TrafficLights import TrafficLights
from TrafficLightsMonitor import TrafficLightsMonitor
from TrafficLightsProgram import TrafficLightsProgram, Phase
from FileManager import FileManager
from ConfigurationInput import ConfigurationInput
from Constants import *
from HelpFunctions import createName

# The path do include the copy of the libraries of SUMO(version 0.15.0)
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), 'tools'))
import sumolib
import traci

def main():
    # Use the global parameters for iteration steps. Maybe their value varies.
    global time_steps
    global min_step
    global max_step

    # Parse the input commands.
    params = ConfigurationInput().parse()

    verbose = False
    if params.has_key(VERBOSE):
        verbose = True

    # If unbounded time step is added, turn the time steps to unlimited
    if params.has_key(UNBOUNDED_STEP):
        time_steps = -1
        min_step = -1
        max_step = -1
    else:
        if params.has_key(STEP_LIMIT):
            steps = int(params[STEP_LIMIT].pop()) 
            if ge(steps, 0):
                time_steps = steps
    
        if params.has_key(START_STEP):
            startStep = int(params[START_STEP].pop())
            if ge(startStep, 0):
                min_step = startStep
    
        if params.has_key(END_STEP):
            endStep = int(params[END_STEP].pop())
            if le(endStep, time_steps):
                max_step = endStep
    
        if ge(max_step, time_steps) or le(max_step, min_step):
            max_step = time_steps
        if ge(min_step, max_step) or ge(min_step, time_steps):
            min_step = 0

    if params.has_key(NET):
        # Open the net file to get the static data from net.
        netFile = params[NET].pop()
        net = sumolib.net.readNet(netFile)
    else:
        # we have a input error.
        print "Error: Parameter -net was not set or parameters are invalid."
        print "Try " + sys.argv[0] + " --help\n"
        exit()
    
    # Blank space is the default format string separator
    separator = ' '
    if params.has_key(SEPARATOR):
        sep = params[SEPARATOR].pop()
        if not eq(sep, None):
            if eq(sep.lower(), TAB):
                separator = '\t'
            elif eq(sep.lower(), BLANK):
                separator = ' '
            elif eq(sep.lower(), COMMA):
                separator = ','

    # Breaks the full option in various type of outputs
    if params.has_key(FULL):
        for key in ALL_PARAMS:
            if not params.has_key(key):
                params[key] = []
        del params[FULL]
    elif (EDGE_PARAMS.isdisjoint(params.keys()) and VEHICLE_PARAMS.isdisjoint(params.keys()) 
          and TRAFFIC_LIGHT_PARAMS.isdisjoint(params.keys()) and NODE_PARAMS.isdisjoint(params.keys())):
        # we have a input error.
        print "Error: You need to choose at least one of output parameters(Vehicle, Edge, Traffic Lights)."
        print "Try " + sys.argv[0] + " --help\n"
        exit()

    if params.has_key(PORT):
        port = int(params[PORT].pop())
        # For the use of SUMO with traci-hub.
        if ge(port, 0):
            traci.init(port)
        else:
            traci.init(DEFAULT_PORT)
    else:
        # For the use of SUMO without traci-hub.
        traci.init(DEFAULT_PORT)

    # If some edges parameter is common
    if not EDGE_PARAMS.isdisjoint(params.keys()):

        # Instantiate the monitor of edges.
        edgeMonitor = EdgeMonitor()
        edgeMonitor.minStep = min_step
        edgeMonitor.maxStep = max_step

        # Search for the edge id's list, and filter it, removing all the id's 
        # that refers to lanes (initiates with ':')
        traciEdgeList = traci.edge.getIDList()
        traciEdgeList = filter(lambda x: x.find(':') == -1, traciEdgeList)

        commonKeys = EDGE_PARAMS.intersection(params.keys())
        edgeIdSet = set()

        # At this point, we have to recognize all the input type for the edges,  
        # if the all parameter for edges is inserted, it is necessary to add all
        # the types of edges output and the list of ids.
        if EDGE_ALL in commonKeys:
            listValues = params.get(EDGE_ALL,[])
            # The key is giving but no parameter, so we need to add some edges
            if eq(len(listValues),0):
                listValues = traciEdgeList
            for key in EDGE_PARAMS.difference(set([EDGE_ALL])):
                edgeMonitor.addEdgesIdOutput(listValues, key)
                params[key] = copy(listValues)
                edgeIdSet.update(listValues)
            del params[EDGE_ALL]
        else:
            for key in commonKeys:
                listValues = params.get(key,'')
                # The key is giving but no parameter, so we need to add some edges
                if eq(len(listValues),0):
                    listValues = traciEdgeList
                edgeMonitor.addEdgesIdOutput(listValues, key)
                params[key] = copy(listValues)
                edgeIdSet.update(listValues)

        # Creates a list with all edge id's that exists and are inserted by user
        edgeIdList = list(edgeIdSet.intersection(traciEdgeList))

        # Warranty that we have some edges to evaluate, taking all the edges
        if eq(len(edgeIdList), 0):
            edgeIdList = traciEdgeList

        # Creates and inserts the initialized edges in the monitor.
        for edgeId in edgeIdList:
            # Ignore every edge that not correspond to a full edge, in that case
            # , the junction lanes.
            if not edgeId.startswith(":"):
                edgeSumoLib = net.getEdge(edgeId)
                fromNode = edgeSumoLib._from._id
                toNode = edgeSumoLib._to._id
                lengthEdge = edgeSumoLib.getLength()
                edge = Edge(edgeId, fromNode, toNode, lengthEdge, verbose)
                edge.minStep = min_step
                edge.maxStep = max_step
                edgeMonitor.addEdge(edge)
    
    if not VEHICLE_PARAMS.isdisjoint(params.keys()):
        # Instantiate the monitor of vehicles.
        vehicleMonitor = VehicleMonitor()
        vehicleMonitor.minStep = min_step
        vehicleMonitor.maxStep = max_step

        # Search for the vehicle id's list.
        traciVehicleList = traci.vehicle.getIDList()

        commonKeys = VEHICLE_PARAMS.intersection(params.keys())
        vehicleIdSet = set()

        # At this point, we have to recognize all the input type for the 
        # vehicles, if the all parameter for vehicles is inserted, it is   
        # necessary to add all the types of vehicles output and the list of ids.
        if (VEHICLE_ALL in commonKeys):
            listValues = params.get(VEHICLE_ALL,[])
            # The key is giving but no parameter, so we need to add some 
            # vehicles.
            if eq(len(listValues),0):
                listValues = traciVehicleList
            for key in VEHICLE_PARAMS.difference(set([VEHICLE_ALL])):
                vehicleMonitor.addVehiclesIdOutput(listValues, key)
                params[key] = copy(listValues)
                vehicleIdSet.update(listValues)
            del params[VEHICLE_ALL]
        else:
            for key in commonKeys:
                listValues = params.get(key,[])
                # The key is giving but no parameter, so we need to add some 
                # vehicles.
                if eq(len(listValues),0):
                    listValues = traciVehicleList
                vehicleMonitor.addVehiclesIdOutput(listValues, key)
                params[key] = copy(listValues)
                vehicleIdSet.update(listValues)

        # Creates a list with all vehicle id's that exists and are inserted by 
        # user.
        vehicleIdList = list(vehicleIdSet.intersection(traciVehicleList))

        # Warranty that we have some vehicles to evaluate, taking all the 
        # vehicles.
        if eq(len(vehicleIdList), 0):
            vehicleIdList = traciVehicleList

        # Creates and inserts the initialized vehicles in the monitor.
        for vehicleId in vehicleIdList:
            if not vehicleMonitor.hasVehicleById(vehicleId):
                vehicle = Vehicle(vehicleId)
                vehicle.minStep = min_step
                vehicle.maxStep = max_step
                vehicle.departure = 0
                vehicleMonitor.addVehicle(vehicle)

    if not TRAFFIC_LIGHT_PARAMS.isdisjoint(params.keys()):
        # Instantiate the monitor of traffic lights.
        trafficLightsMonitor = TrafficLightsMonitor()
        trafficLightsMonitor.minStep = min_step
        trafficLightsMonitor.maxStep = max_step

        # Search for the traffic lights id's list.
        traciTrafficLightsList = traci.trafficlights.getIDList()

        commonKeys = TRAFFIC_LIGHT_PARAMS.intersection(params.keys())
        trafficLightsIdSet = set()

        # At this point, we have to recognize all the input type for the traffic
        # lights, if the all parameter for traffic lights is inserted, it is   
        # necessary to add all the types of traffic lights output and the list 
        # of ids.
        if TRAFFIC_LIGHT_ALL in commonKeys:
            listValues = params.get(TRAFFIC_LIGHT_ALL,[])
            # The key is giving but no parameter, so we need to add some traffic
            # lights
            if eq(len(listValues),0):
                listValues = traciTrafficLightsList
            for key in TRAFFIC_LIGHT_PARAMS.difference(set([TRAFFIC_LIGHT_ALL])):
                trafficLightsMonitor.addTrafficLightsIdOutput(listValues, key)
                params[key] = copy(listValues)
                trafficLightsIdSet.update(listValues)
            del params[TRAFFIC_LIGHT_ALL]
        else:
            for key in commonKeys:
                listValues = params.get(key,'')
                # The key is giving but no parameter, so we need to add some 
                # traffic lights
                if eq(len(listValues),0):
                    listValues = traciTrafficLightsList
                trafficLightsMonitor.addTrafficLightsIdOutput(listValues, key)
                params[key] = copy(listValues)
                trafficLightsIdSet.update(listValues)

        # Creates a list with all traffic lights id's that exists and are 
        # inserted by user
        trafficLightsIdList = list(trafficLightsIdSet.intersection(traciTrafficLightsList))

        # Warranty that we have some traffic lights to evaluate, taking all the 
        # traffic lights
        if eq(len(trafficLightsIdList), 0):
            trafficLightsIdList = traciTrafficLightsList

        for trafficLightsId in trafficLightsIdList:
            # Instantiate the traffic lights object and add some data.
            trafficLights = TrafficLights(trafficLightsId)
            # Simulation steps interval
            trafficLights.minStep = min_step
            trafficLights.maxStep = max_step
            # Controlled lanes
            trafficLights.controlledLanes = traci.trafficlights.getControlledLanes(trafficLightsId)
            # Controlled links
            trafficLights.controlledLinks = traci.trafficlights.getControlledLinks(trafficLightsId)

            # Complete logic and phases of the semaphore
            programList = traci.trafficlights.getCompleteRedYellowGreenDefinition(trafficLightsId)

            # Take the first and unique program in the list
            while len(programList) > 0:
                phases = []
                program = programList.pop()
                if program:
                    # Instantiate the logic program helper class for traffic 
                    # lights.
                    trafficLightsProgram = TrafficLightsProgram()
                    trafficLightsProgram.id = program._subID
                    trafficLightsProgram.programType = program._type
                    trafficLightsProgram.subParameter = program._subParameter
                    trafficLightsProgram.currentPhaseIndex = program._currentPhaseIndex

                    # Take the phases of the signal state
                    for phase in program._phases:
                        ph = Phase(phase._duration, phase._duration1, phase._duration2, phase._phaseDef)
                        phases.append(ph)
                    trafficLightsProgram.phases = phases

                    # Adds the semaphore program to the traffic lights
                    trafficLights.addLogicProgram(trafficLightsProgram)

            # Inserts the initialised traffic lights in the monitor.
            trafficLightsMonitor.addTrafficLights(trafficLights)

    if not NODE_PARAMS.isdisjoint(params.keys()):
        pass

## reroute test
#    traci.route.add(
#       "sp_route1", 
#       ["south/center", "center/north", "north/center", "center/south"]
#    )
#    traci.route.add(
#       "sp_route2", 
#       ["center/south", "south/center", "center/north", "north/center"]
#    )
#    traci.route.add(
#       "sp_route3", 
#       ["north/center", "center/south", "south/center", "center/north"]
#    )
#    traci.route.add(
#       "sp_route4", 
#       ["center/north", "north/center", "center/south","south/center"]
#    )
#    traci.vehicle.add("special", "sp_route1", 0)

    # For each iteration of the simulation.
    timeStep = 0
    timeStepFinal = 0

    # Creating the clone summary output
    data = ["#step"]
    data.append("loaded")
    data.append("departed")
    data.append("running")
    data.append("arrived")
    summaryData = [separator.join(data)]

    totalLoaded = 0
    totalDeparted = 0
    totalArrived = 0

    #
    # Simulation beginning
    #
    while True:

        # All vehicles have arrived
        if timeStep > 5 and totalArrived == totalDeparted:
            traci.close()
            break

        # The maximum time step has been reached
        if not eq(time_steps,-1) and gt(timeStep, max_step):
            traci.close()
            break

        try:

            # Executes one step
            traci.simulationStep()

            totalLoaded += traci.simulation.getLoadedNumber()
            totalDeparted += traci.simulation.getDepartedNumber()
            totalArrived += traci.simulation.getArrivedNumber()
            totalRunning = totalDeparted - totalArrived

            data = []   # clear list
            data.append(str(timeStep))
            data.append(str(totalLoaded))
            data.append(str(totalDeparted))
            data.append(str(totalRunning))
            data.append(str(totalArrived))
            summaryData.append(separator.join(data))

#            # All vehicles have arrived
#            if timeStep > 5 and totalArrived == totalDeparted:
#                traci.close()
#                break
#
#            # The maximum time step has been reached
#            if not eq(time_steps,-1) and gt(timeStep, max_step):
#                traci.close()
#                break

#        except traci.FatalTraCIError as message:
#            print message
#            traci.close()
#            #exit()
#            break

            # One step execution of evaluation
            if (ge(timeStep, min_step) and le(timeStep, max_step)) or eq(time_steps,-1):
                if not EDGE_PARAMS.isdisjoint(params.keys()):
                    # Updates the edges in the monitor with the data of simulation 
                    # in this step.
                    for edgeId in edgeIdList:
                        edgeMonitor.updateEdge(
                                               timeStep, edgeId,
                                               traci.edge.getLastStepVehicleNumber(edgeId),
                                               traci.edge.getLastStepMeanSpeed(edgeId),
                                               traci.edge.getLastStepHaltingNumber(edgeId),
                                               traci.edge.getLastStepLength(edgeId),
                                               traci.edge.getLastStepOccupancy(edgeId)
                                               )
                if not VEHICLE_PARAMS.isdisjoint(params.keys()):
                    # Search for the vehicle id's list.
                    traciVehicleList = traci.vehicle.getIDList()
     
                    commonKeys = VEHICLE_PARAMS.intersection(params.keys())
                    vehicleIdSet = set()
    
                    for key in commonKeys:
                        listValues = params.get(key,[])
    
                        # The key is giving but no parameter, so we need to add some 
                        # vehicles
                        if not listValues:
                            # Takes the actual list of vehicles in simulation
                            listValues = traciVehicleList
                            # and adds to the output list.
                            vehicleMonitor.addVehiclesIdOutput(listValues, key)
    
                        vehicleIdSet.update(listValues)
    
                    # Creates a list with all vehicle id's that exists and are 
                    # inserted by user
                    vehicleIdList = list(vehicleIdSet)
    
                    # Warranty that we have some vehicles to evaluate, taking all 
                    # the vehicles
                    if not vehicleIdList:
                        vehicleIdList = traciVehicleList
    
                    # Creates and inserts the initialized vehicles in the monitor.
                    # Updates the vehicles in the monitor with the data of 
                    # simulation in this step.
                    for vehicleId in vehicleIdList:
                        if not vehicleMonitor.hasVehicleById(vehicleId):
                            # Insert the new vehicle
                            vehicle = Vehicle(vehicleId)
                            vehicle.minStep = min_step
                            vehicle.maxStep = max_step
                            vehicle.departure = timeStep
                            vehicleMonitor.addVehicle(vehicle)
    
    #                    #reroute test
    #                    if "special" in vehicleIdList:
    #                        #print traci.vehicle.getRoadID("special")
    #                        if traci.vehicle.getRoadID("special") == "south/center":
    #                            traci.vehicle.setRouteID("special", "sp_route1")
    #                        elif traci.vehicle.getRoadID("special") == "center/north":
    #                            traci.vehicle.setRouteID("special", "sp_route4")
    #                        elif traci.vehicle.getRoadID("special") == "north/center":
    #                            traci.vehicle.setRouteID("special", "sp_route3")
    #                        elif traci.vehicle.getRoadID("special") == "center/south":
    #                            traci.vehicle.setRouteID("special", "sp_route2")
    
                    #TODO: ainda precisa corrigir aqui, para evitar que o '-' fique sendo inserido regularmente
                    for vehicleId in vehicleMonitor.getVehiclesIdList():
                        # The current simulation vehicles
                        if vehicleId in traci.vehicle.getIDList():
                            edgeId = traci.vehicle.getRoadID(vehicleId)
                            if net.hasEdge(edgeId):
                                edgeLength = net.getEdge(edgeId).getLength()
                            else:
                                edgeId = '-'
                                edgeLength = 0
    
                            vehicleMonitor.updateVehicle(
                                                   timeStep, vehicleId,
                                                   traci.vehicle.getSpeed(vehicleId),
                                                   traci.vehicle.getRouteID(vehicleId),
                                                   traci.vehicle.getRoute(vehicleId),
                                                   edgeId, edgeLength
                                                   )
    
                    for vehicleId in traci.simulation.getArrivedIDList():
                        if vehicleMonitor.hasVehicleById(vehicleId):
                            vehicleMonitor.updateArrivedVehicle(timeStep, vehicleId)
                    timeStepFinal +=1
    
                if not TRAFFIC_LIGHT_PARAMS.isdisjoint(params.keys()):
                    # Updates the traffic lights in the monitor with the data of 
                    # simulation in this step.
                    for trafficLightsId in trafficLightsIdList:
                        lanes = trafficLightsMonitor.getTrafficLightsLanesById(trafficLightsId)
                        haltingVehicles = [traci.lane.getLastStepHaltingNumber(laneId) for laneId in lanes]
                        trafficLightsMonitor.updateTrafficLights(
                                                                 timeStep,
                                                                 trafficLightsId,
                                                                 haltingVehicles
                                                                 )
    
                # dynamics
    #            # assumed time to next switch
    #            traci.trafficlights.getNextSwitch(trafficLightsId)
    #            # index of the current phase index request
    #            traci.trafficlights.getPhase(trafficLightsId)
    #            # traffic light states, encoded as rRgGyYoO
    #            print traci.trafficlights.getRedYellowGreenState(trafficLightsId)
    #                    trafficLightsMonitor.updateEdge(
    #                                           timeStep, trafficLightsId
    #                                           )
    
                if not NODE_PARAMS.isdisjoint(params.keys()):
                    pass
    
            timeStep += 1

        # End of simulation by closing the SUMO simulator.
        except traci.FatalTraCIError as message:
            print message
            traci.close()
            #exit()
            break

    # After completed the generation of data for the simulation, save in the file.
    uniqueId = str(abs(hash(random())))

    # summary copy output
    fileSummary = FileManager(createName(uniqueId, '', summary=True))
    fileSummary.addData("\n".join(summaryData))

    # Instantiate the file objects for future manipulate.
    if not EDGE_PARAMS.isdisjoint(params.keys()):
        fileEval = FileManager(createName(uniqueId, EDGE_ALL, True))
        fileEval.addData(edgeMonitor.toStringEvaluate(separator))
        for param in EDGE_PARAMS:
            if params.has_key(param):
                fileBase = FileManager(createName(uniqueId, param))
                fileBase.addData(edgeMonitor.toString(param,separator))

    if not VEHICLE_PARAMS.isdisjoint(params.keys()):
        # TODO: needs a verification
        # Update all the vehicles arrived time for vehicles that not have really
        # arrived at end of simulation.
        vehicleMonitor.update(timeStepFinal)
        fileEval = FileManager(createName(uniqueId, VEHICLE_ALL, True))
        fileEval.addData(vehicleMonitor.toStringEvaluate(separator))
        for param in VEHICLE_PARAMS:
            if params.has_key(param):
                fileBase = FileManager(createName(uniqueId, param))
                fileBase.addData(vehicleMonitor.toString(param,separator))

    if not TRAFFIC_LIGHT_PARAMS.isdisjoint(params.keys()):
        fileEval = FileManager(createName(uniqueId, TRAFFIC_LIGHT_ALL, True))
        fileEval.addData(trafficLightsMonitor.toStringEvaluate(separator))
        for param in TRAFFIC_LIGHT_PARAMS:
            if params.has_key(param):
                fileBase = FileManager(createName(uniqueId, param))
                fileBase.addData(trafficLightsMonitor.toString(param,separator))

    if not NODE_PARAMS.isdisjoint(params.keys()):
        # TODO: need development
        pass

    exit()

if __name__ == '__main__':
    main()
