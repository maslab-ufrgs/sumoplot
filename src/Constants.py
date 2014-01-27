#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# Global variables.
#
time_steps = 10000
"""Total time steps for simulation."""
min_step = 0
"""Minimum time step to extract data."""
max_step = time_steps
"""Maximum time step to extract data."""

#
# Constants
#

# For Simulation
DEFAULT_PORT = 8813
"""Standardized port to connection with the SUMO."""

# For Configuration options
HELP = '--help'
PORT = '--port'
MIN_PORT = '-p'
FULL = '--full'
MIN_FULL = '-f' 
NET = '--net'
MIN_NET = '-n'
VERBOSE = '--verbose'
MIN_VERBOSE = '-v'
STEP_LIMIT = '--step-limit'
MIN_STEP_LIMIT = '-sl'
START_STEP = '--step-start'
MIN_START_STEP = '-ss'
END_STEP = '--step-end'
MIN_END_STEP = '-se'
UNBOUNDED_STEP = '--step-unbounded'
MIN_UNBOUNDED_STEP = '-su'
SEPARATOR = '--separator'
MIN_SEPARATOR = '-s'

# Todo: Waiting development for xml input and model output
#CONFIG = '--config'
#MODEL = '--model'

# String format
TAB = 'tab'
BLANK = 'blank'
COMMA = 'comma'

# For Edge and EdgeMonitor
EDGES = 'Edges'
VEHICLE_NUMBER = 'Edges.Vehicle.Number'
MEAN_SPEED = 'Edges.Mean.Speed'
HALTING_NUMBER = 'Edges.Halting.Number'
JAM_LENGTH = 'Edges.Jam.Length'
OCCUPATION = 'Edges.Occupation'
EDGE_ALL = '--edge-all'
MIN_EDGE_ALL = '-ea'
EDGE_VEHICLE_NUMBER = '--edge-vehicle'
MIN_EDGE_VEHICLE_NUMBER = '-ev'
EDGE_MEAN_SPEED = '--edge-speed'
MIN_EDGE_MEAN_SPEED = '-es'
EDGE_HALTING_NUMBER = '--edge-halting'
MIN_EDGE_HALTING_NUMBER = '-eh'
EDGE_JAM_LENGTH = '--edge-length'
MIN_EDGE_JAM_LENGTH = '-el'
EDGE_OCCUPATION = '--edge-occupation'
MIN_EDGE_OCCUPATION = '-eo'

# For Vehicle and VehicleMonitor
VEHICLES = 'Vehicles'
SPEED = 'Vehicles.Mean.Speed'
ROUTE = 'Vehicles.Route'
DISTANCE = 'Vehicles.Distance'
TIME = 'Vehicles.Time'
VEHICLE_ALL = '--vehicle-all'
MIN_VEHICLE_ALL = '-va'
VEHICLE_SPEED = '--vehicle-speed'
MIN_VEHICLE_SPEED = '-vs'
VEHICLE_ROUTE = '--vehicle-route'
MIN_VEHICLE_ROUTE = '-vr'
VEHICLE_DISTANCE = '--vehicle-distance'
MIN_VEHICLE_DISTANCE = '-vd'
VEHICLE_TIME = '--vehicle-time'
MIN_VEHICLE_TIME = '-vt'

# For Nodes
NODES = 'Nodes'
NODE_ALL = '--node-all'
MIN_NODE_ALL = '-na'

# For Traffic lights
TRAFFIC_LIGHTS = 'Traffic.Lights'
HALTING = 'Traffic.Lights.Halting.Number'
TRAFFIC_LIGHT_ALL = '--tls-all'
MIN_TRAFFIC_LIGHT_ALL = '-tla'
TRAFFIC_LIGHT_HALTING = '--tls-halting'
MIN_TRAFFIC_LIGHT_HALTING = '-tlh'

# Sets of global constants
EDGE_PARAMS = frozenset([EDGE_ALL,EDGE_VEHICLE_NUMBER,EDGE_MEAN_SPEED,EDGE_HALTING_NUMBER,EDGE_JAM_LENGTH,EDGE_OCCUPATION])
"""All options for edges."""

VEHICLE_PARAMS = frozenset([VEHICLE_ALL, VEHICLE_SPEED, VEHICLE_ROUTE, VEHICLE_DISTANCE, VEHICLE_TIME])
"""All options for vehicles."""

TRAFFIC_LIGHT_PARAMS = frozenset([TRAFFIC_LIGHT_ALL,TRAFFIC_LIGHT_HALTING])
"""All options for traffic lights."""

NODE_PARAMS = frozenset([NODE_ALL])
"""All options for nodes."""

ALL_PARAMS = frozenset([EDGE_ALL,NODE_ALL,VEHICLE_ALL,TRAFFIC_LIGHT_ALL])
"""All options in one set."""