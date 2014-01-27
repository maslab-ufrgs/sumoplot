#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

class FileManager(object):
    """Class responsible to manipulate files and to save simulation data."""

    def __init__(self, fileName='saida.txt'):
        """Output path of the simulation."""
        self._filePath = os.path.join(os.getcwd(),os.path.dirname(__file__), "../output")
        """Output file of the simulation data file."""
        self._fileOut = os.path.join(self._filePath, fileName)
        """The pointer for the output file."""
        self._filePointer = None

        # Create the output folder if it not exists
        if not os.path.exists(self._filePath):
            os.makedirs(self._filePath)

        if not os.path.exists(self._fileOut):
            print "\nA file with the results has been created and saved in: '%s'" % self._fileOut
            file(self._fileOut, 'w').close()
        else:
            if not os.path.isfile(self._fileOut):
                print "\nA file with the results has been created and saved in: '%s'" % self._fileOut
                file(self._fileOut, 'w').close()

    def open(self):
        """Open the file in append mode and keep the pointer to it."""
        self._filePointer = open(self._fileOut,'a')

    def close(self):
        """Close the file using the self pointer of manager."""
        self._filePointer.close()

    def addData(self, data):
        """Add data to the final of the file, the file is open and closed by the
        method every time he is called.
        """
        self.open()
        self._filePointer.write(data)
        self.close()

    def new(self):
        """Clear the file, creating a new file in the same local. Uses the write
        mode of File base class. Closes the file after.
        """
        self._filePointer = open(self._fileOut,'w')
        self.close()
