#!/bin/bash

netgen --grid --grid.number 3 --grid.length 200 --output-file grid2.net.xml --default.lanenumber 1 --default-junction-type traffic_light --no-turnarounds

#randomTrips.py
# randomTrips.py -n grid2.net.xml -o grid2.trips.xml -r grid2.rou.xml -e 700 -l -L -v