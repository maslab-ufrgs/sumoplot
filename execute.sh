#!/bin/bash

###################################
# Traffic Lights tests
###################################
#sumo-gui -c network/default/ti.sumo.cfg --summary sumario.xml & python sumoplot.py --net network/default/ti.net.xml -tla -sl 500 -ss 0 -se 500

###################################
# Vehicle tests
###################################
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml -vs t366 t42 -sl 100 -ss 0 -se 100
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml -va -sl 300 -ss 0 -se 300
#sumo-gui -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml -va --step-unbounded --separator tab
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml -va special t375 -sl 500 -ss 100 -se 500

###################################
# Edge tests
###################################
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py -n network/default/ti.net.xml --edge-halting -sl 500 -ss 200 --edge-vehicle -ea center/east --separator comma
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py -n network/default/ti.net.xml --port 500 -ss 1000 --separator comma --edge-all center/nw center/nw
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py -n network/default/ti.net.xml -sl 100 -ss 100 -se 400 --edge-halting center/east center/north center/nw --edge-vehicle --separator blank
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py -n network/default/ti.net.xml -ss 10001 -se 11000 --edge-halting --edge-vehicle --separator comma

###################################
# The default examples
###################################
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --help
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --edge-all
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py -n network/default/ti.net.xml -ea
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --edge-halting center/east center/north center/nw --edge-vehicle center/east center/north center/nw
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --edge-halting --edge-vehicle center/east center/nw
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml -es --separator comma
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --step-limit 500 --step-start 100 --step-end 400 --edge-length center/east center/north center/nw --separator tab
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --step-limit 500 --step-start 100 --step-end 400 --edge-halting center/east center/north center/nw --separator tab

###################################
# Full operations tests
###################################
sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --full -sl 700 -ss 0 -se 700

###################################
# Multi observer tests
###################################
#sumo -c network/default/ti.sumo.cfg & python sumoplot.py --net network/default/ti.net.xml --vehicle-speed special t375 -vr special t375 --edge-length center/east center/nw -sl 2000 -ss 100 -se 1600
