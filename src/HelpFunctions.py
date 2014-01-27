#!/usr/bin/env python
#-*- coding: utf-8 -*-

from operator import eq
from Constants import *

def exists(var):
    """Verify the existence of an variable and return an boolean."""
    try:
        var
        return True
    except NameError:
        return False

def createName(uniqueId, pattern, evaluate=False, summary=False):
    """Concatenate some words to form an string name used in the file 
    simulation output and return the string.

    Keyword arguments:
    uniqueId -- an string identifier representing a unique time stamp
    pattern -- some constant defined for the Edge, Vehicle, Traffic Lights or
        Node class
    evaluate -- a boolean flag to evaluate name output

    """
    name = [uniqueId]
    # Edges
    if eq(pattern,EDGE_ALL):
        name.append(EDGES)
    elif eq(pattern,EDGE_VEHICLE_NUMBER):
        name.append(VEHICLE_NUMBER)
    elif eq(pattern,EDGE_MEAN_SPEED):
        name.append(MEAN_SPEED)
    elif eq(pattern,EDGE_HALTING_NUMBER):
        name.append(HALTING_NUMBER)
    elif eq(pattern,EDGE_JAM_LENGTH):
        name.append(JAM_LENGTH)
    elif eq(pattern,EDGE_OCCUPATION):
        name.append(OCCUPATION)
    # Vehicles
    elif eq(pattern,VEHICLE_ALL):
        name.append(VEHICLES)
    elif eq(pattern,VEHICLE_SPEED):
        name.append(SPEED)
    elif eq(pattern,VEHICLE_ROUTE):
        name.append(ROUTE)
    elif eq(pattern,VEHICLE_DISTANCE):
        name.append(DISTANCE)
    elif eq(pattern,VEHICLE_TIME):
        name.append(TIME)
    # Traffic Lights
    elif eq(pattern,TRAFFIC_LIGHT_ALL):
        name.append(TRAFFIC_LIGHTS)
    elif eq(pattern,TRAFFIC_LIGHT_HALTING):
        name.append(HALTING)

    # Other evaluates about simulation
    if eq(evaluate, True):
        name.append('Evaluate')

    if eq(summary, True):
        name.append('Summary')

    name.append('csv')
    return '.'.join(name)

def formatListOutput(itemslist, separator=';'):
    """Return a formated string based in the items elements.

    Keyword arguments:
    itemslist -- an list of strings to format
    separator -- an string to separate the string items

    """
    saida = []
    saida.append('[')
    if itemslist:
        values = []
        for item in itemslist:
            values.append(item)
        saida.append(separator.join(values))
    saida.append(']')
    return ''.join(saida)
