#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy

class TrafficLightsProgram(object): #Logic
    """Class responsible for handling one Traffic Lights Program object."""

    def __init__(self, programId = 0, programType = 0, subParameter = 0, currentPhaseIndex = 0):
        """Identifies the Traffic Lights Program object."""
        self._programId = programId
        """Keeps the type of the Traffic Lights Program. eg. static, actuated, 
        agentbased.
        """
        self._type = programType
        """Keeps the sub parameter of the Traffic Lights Program."""
        self._subParameter = subParameter
        """Keeps the current phase index (sequential number of the phases) of 
        the Traffic Lights Program.
        """
        self._currentPhaseIndex = currentPhaseIndex
        """Keeps a list of phases (signal states) of the Traffic Lights Program."""
        self._phases = []

    @property
    def id(self):
        """Return the identifier of the Traffic Lights Program as an string."""
        return self._programId

    @id.setter
    def id(self, programId):
        """Update the identifier of the Traffic Lights Program."""
        self._id = programId

    @property
    def programType(self):
        """Return the type of the Traffic Lights Program as an string."""
        return self._type

    @programType.setter
    def programType(self, programType):
        """Update the type of the Traffic Lights Program."""
        self._type = programType

    @property
    def subParameter(self):
        """Return the sub parameter of the Traffic Lights Program as an string."""
        return self._subParameter

    @subParameter.setter
    def subParameter(self, subParameter):
        """Update the sub parameter of the Traffic Lights Program."""
        self._subParameter = subParameter

    @property
    def currentPhaseIndex(self):
        """Return the current phase index (sequential number of the phases) of 
        the Traffic Lights Program as an integer."""
        return self._currentPhaseIndex

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, currentPhaseIndex):
        """Update the current phase index (sequential number of the phases) of 
        the Traffic Lights Program."""
        self._currentPhaseIndex = currentPhaseIndex

    @property
    def phases(self):
        """Return a list of Phase objects of the Traffic Lights Program."""
        return copy.deepcopy(self._phases)

    @phases.setter
    def phases(self, phases):
        """Update the list of Phase objects of the Traffic Lights Program."""
        self._phases = copy.deepcopy(phases)

    def addPhase(self, phase):
        """Add a Phase object to the Traffic Lights Program."""
        self._phases.append(phase)

    def __str__(self):
        data = []
        data.append('#id='+str(self.id)+'\n')
        data.append('#programType='+str(self.programType)+'\n')
        data.append('#subParameter='+str(self.subParameter)+'\n')
        data.append('#currentPhaseIndex='+str(self.currentPhaseIndex)+'\n')
        for phase in self.phases:
            data.append(str(phase))
            data.append('\n')

        return ''.join(data)

class Phase(object):
    """Class responsible for handling one Traffic Lights Program Phase."""

    def __init__(self, duration, duration1, duration2, definition):
        self._duration = duration
        self._duration1 = duration1
        self._duration2 = duration2
        self._phaseDef = definition

    @property
    def duration(self):
        """Return the current duration time for the Phase of the plan semaphore
        as an integer.
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Overwrite the current duration time for the Phase of the plan 
        semaphore.
        """
        self._duration = duration

    @property
    def duration1(self):
        """Return the minimum duration time for the Phase of the plan semaphore
        as an integer.
        """
        return self._duration1

    @duration1.setter
    def duration1(self, duration):
        """Overwrite the minimum duration time for the Phase of the plan 
        semaphore.
        """
        self._duration1 = duration

    @property
    def duration2(self):
        """Return the maximum duration time for the Phase of the plan semaphore
        as an integer.
        """
        return self._duration2

    @duration2.setter
    def duration2(self, duration):
        """Overwrite the maximum duration time for the Phase of the plan 
        semaphore.
        """
        self._duration2 = duration

    @property
    def definition(self):
        """Return the definition color signals for the Phase of the plan 
        semaphore as an string.
        """
        return self._phaseDef

    @definition.setter
    def definition(self, definition):
        """Overwrite the definition color signals for the Phase of the plan 
        semaphore.
        """
        self._phaseDef = definition

    def __str__(self):
        data = []
        data.append('#duration='+str(self.duration)+'\n')
        data.append('#duration1='+str(self.duration1)+'\n')
        data.append('#duration2='+str(self.duration2)+'\n')
        data.append('#definition='+self.definition+'\n')

        return ''.join(data)