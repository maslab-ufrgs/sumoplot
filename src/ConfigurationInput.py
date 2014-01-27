#!/usr/bin/env python
#-*- coding: utf-8 -*-
import argparse
from Constants import *

class ConfigurationInput(object):
    """Class that does the initial treatment of input parameters on the command 
    line, separate them and organizes a dictionary easily usable.
    """

    def __init__(self):
        pass

    def parse(self):
        """Read the input string and put the arguments in a dictionary."""

        parser = argparse.ArgumentParser(description='Extract some data from SUMO simulation, based on the input parameters.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument(MIN_NET, NET, dest=NET, nargs=1, required=True, help='Captures the file containing the network to be simulated, to obtain data.')
        parser.add_argument(MIN_SEPARATOR, SEPARATOR, dest=SEPARATOR, nargs=1, metavar='type', default=BLANK, choices=[TAB, BLANK, COMMA], help='Flag to inform how the output data should be separated.')
        parser.add_argument(MIN_PORT, PORT, dest=PORT, nargs=1, metavar='number', default=DEFAULT_PORT, help='Flag to inform the port to communicate with traci-hub or SUMO.')
        parser.add_argument(MIN_VERBOSE, VERBOSE, dest=VERBOSE, action='store_const', const='', help='Flag to show or not execution messages.')
        
        parser.add_argument(MIN_FULL, FULL, dest=FULL, action='store_const', const='', help='Flag to output multiple file results, for the types of simulation, like edges, nodes, vehicles and traffic lights.')

        #TODO: Waiting for development
        #parser.add_argument('-m', MODEL, dest=MODEL, help='Flag to create file default model to input program.')
        #parser.add_argument('-c', CONFIG, dest=CONFIG, nargs=1, metavar='file', type=file, help='Captures the file containing the configuration for obtaining the simulation data.')
        
        groupStep = parser.add_argument_group('Steps control group','The commands that manipulate the simulation steps.')
        groupStep.add_argument(MIN_STEP_LIMIT, STEP_LIMIT, dest=STEP_LIMIT, nargs=1, type=int, metavar='number', default=time_steps, help='The total step interval for capture of the simulation data.')
        groupStep.add_argument(MIN_START_STEP, START_STEP, dest=START_STEP, nargs=1, type=int, metavar='number', default=min_step, help='The start step interval for capture of the simulation data.')
        groupStep.add_argument(MIN_END_STEP, END_STEP, dest=END_STEP, nargs=1, type=int, metavar='number', default=max_step, help='The end step interval for capture of the simulation data.')
        groupStep.add_argument(MIN_UNBOUNDED_STEP, UNBOUNDED_STEP, dest=UNBOUNDED_STEP, action='store_const', const='', help='A flag to identify that the simulation will have no limit of steps, and will end according to the SUMO cfg file.')

        groupEdge = parser.add_argument_group('Edge group','The parameters that define the focus of simulation and extraction data.')
        groupEdge.add_argument(MIN_EDGE_ALL, EDGE_ALL, dest=EDGE_ALL, nargs='*', metavar='edgeId', help='Parameter responsible for the extraction of all the information related to the edges.')
        groupEdge.add_argument(MIN_EDGE_VEHICLE_NUMBER, EDGE_VEHICLE_NUMBER, dest=EDGE_VEHICLE_NUMBER, nargs='*', metavar='edgeId', help='Parameter responsible for the extraction of information on the number of vehicles that passed through the edge.')
        groupEdge.add_argument(MIN_EDGE_MEAN_SPEED, EDGE_MEAN_SPEED, dest=EDGE_MEAN_SPEED, nargs='*', metavar='edgeId', help='Parameter responsible for the extraction of information on the average speed of vehicles that passed through the edge.')
        groupEdge.add_argument(MIN_EDGE_HALTING_NUMBER, EDGE_HALTING_NUMBER, dest=EDGE_HALTING_NUMBER, nargs='*', metavar='edgeId', help='Parameter responsible for the extraction of information on the number of vehicles that were at a traffic jam on the edge.')
        groupEdge.add_argument(MIN_EDGE_JAM_LENGTH, EDGE_JAM_LENGTH, dest=EDGE_JAM_LENGTH, nargs='*', metavar='edgeId', help='Parameter responsible for the extraction of information on the total length of vehicles that were at a traffic jam on the edge.')
        groupEdge.add_argument(MIN_EDGE_OCCUPATION, EDGE_OCCUPATION, dest=EDGE_OCCUPATION, nargs='*', metavar='edgeId', help='Occupation.')

        groupVehicle = parser.add_argument_group('Vehicle group','The parameters that define the focus of simulation and extraction data.')
        groupVehicle.add_argument(MIN_VEHICLE_ALL, VEHICLE_ALL, dest=VEHICLE_ALL, nargs='*', metavar='vehicleId', help='Parameter responsible for the extraction of all the information related to the vehicles.')
        groupVehicle.add_argument(MIN_VEHICLE_DISTANCE, VEHICLE_DISTANCE, dest=VEHICLE_DISTANCE, nargs='*', metavar='vehicleId', help='Parameter responsible for the extraction of information on the travel distance by the vehicles.')
        groupVehicle.add_argument(MIN_VEHICLE_TIME, VEHICLE_TIME, dest=VEHICLE_TIME, nargs='*', metavar='vehicleId', help='Parameter responsible for the extraction of information on the travel time by the vehicles.')
        groupVehicle.add_argument(MIN_VEHICLE_SPEED, VEHICLE_SPEED, dest=VEHICLE_SPEED, nargs='*', metavar='vehicleId', help='Parameter responsible for the extraction of information on the mean speed of the vehicles.')
        groupVehicle.add_argument(MIN_VEHICLE_ROUTE, VEHICLE_ROUTE, dest=VEHICLE_ROUTE, nargs='*', metavar='vehicleId', help='Parameter responsible for the extraction of information on the route of the vehicles.')

        groupTls = parser.add_argument_group('Traffic Light group','The parameters that define the focus of simulation and extraction data.')
        groupTls.add_argument(MIN_TRAFFIC_LIGHT_ALL, TRAFFIC_LIGHT_ALL, dest=TRAFFIC_LIGHT_ALL, nargs='*', metavar='tlsId', help='Parameter responsible for the extraction of all the information related to the traffic lights.')
        groupTls.add_argument(MIN_TRAFFIC_LIGHT_HALTING, TRAFFIC_LIGHT_HALTING, dest=TRAFFIC_LIGHT_HALTING, nargs='*', metavar='tlsId', help='Parameter responsible for the extraction of the information on the number of vehicles stopped at every lane controlled by the traffic lights.')

        #TODO: Waiting for development        
        #groupNode = parser.add_argument_group('Node group','The parameters that define the focus of simulation and extraction data.')
        #groupNode.add_argument('-na', NODE_ALL, dest=NODE_ALL, nargs='*', metavar='nodeIdList', help='Obtains the goal result of simulation.')

        args = parser.parse_args()
        params = vars(args)

        # Remove the parameter not inserted in the input.
        for key,value in params.items():
            if value is None:
                del params[key]
            elif not isinstance(value, list):
                params[key] = []
                params[key].append(value)

        return params