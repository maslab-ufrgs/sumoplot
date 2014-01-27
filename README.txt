@author: Alessandro Dalla Vecchia
sumoplot (c) 2012 Alessandro Dalla Vecchia, 
Laboratório de Sistemas Multi-Agentes
Instituto de Informática da Universidade Federal do Rio Grande do Sul

This folder contains some classes of help to extract and manipulate results for
the SUMO simulation.

The requirements for use are: Python version 2.7.* and external module numpy.
The numpy can be installed in Ubuntu via synaptic.

A user wiki can be acessed here: https://wiki.inf.ufrgs.br/Sumoplot

/FOLDERS
--------

- /network
    The folder "network" keeps an network example with be used for test of the
program execution. It's only for reference.

- /output
    The folder "output" keeps the execution output of the program. For avoid
superscript in parallel executions, the files are named using a first
identification based in a time stamp.

- /src
    The folder "src" keeps the source scripts of the application. It's a group
of python classes that extract information of simulation, manipulate data,
objects and files.

- /tools
    The folder "tools" keeps some copies of the tools libraries of the SUMO(
version 0.15.0), like traci and sumolib, because they are necessary for the
execution of the scripts.

COMMANDS SUPPORTED (copy of --help option)
------------------

usage: sumoplot.py [-h] -n file [-s type] [-p number] [-f] [-sl number]
                   [-ss number] [-se number] [-su] [-ea [edgeId [edgeId ...]]]
                   [-ev [edgeId [edgeId ...]]] [-es [edgeId [edgeId ...]]]
                   [-eh [edgeId [edgeId ...]]] [-el [edgeId [edgeId ...]]]
                   [-va [vehicleId [vehicleId ...]]]
                   [-vd [vehicleId [vehicleId ...]]]
                   [-vt [vehicleId [vehicleId ...]]]
                   [-vs [vehicleId [vehicleId ...]]]
                   [-vr [vehicleId [vehicleId ...]]]
                   [-tla [tlsId [tlsId ...]]] [-tlh [tlsId [tlsId ...]]]

Extract some data from SUMO simulation, based on the input parameters.

optional arguments:
  -h, --help            show this help message and exit
  -n file, --net file   Captures the file containing the network to be
                        simulated, to obtain data. (default: None)
  -s type, --separator type
                        Flag to inform how the output data should be
                        separated. (default: blank)
  -p number, --port number
                        Flag to inform the port to communicate with traci-hub
                        or SUMO. (default: 8813)
  -f, --full            Flag to output multiple file results, for the types of
                        simulation, like edges, nodes, vehicles and traffic
                        lights. (default: None)

Steps control group:
  The commands that manipulate the simulation steps.

  -sl number, --step-limit number
                        The total step interval for capture of the simulation
                        data. (default: 10000)
  -ss number, --step-start number
                        The start step interval for capture of the simulation
                        data. (default: 0)
  -se number, --step-end number
                        The end step interval for capture of the simulation
                        data. (default: 10000)
  -su, --step-unbounded
                        A flag to identify that the simulation will have no
                        limit of steps, and end when the SUMO stop. (default:
                        None)

Edge group:
  The parameters that define the focus of simulation and extraction data.

  -ea [edgeId [edgeId ...]], --edge-all [edgeId [edgeId ...]]
                        Parameter responsible for the extraction of all the
                        information related to the edges. (default: None)
  -ev [edgeId [edgeId ...]], --edge-vehicle [edgeId [edgeId ...]]
                        Parameter responsible for the extraction of
                        information on the number of vehicles that passed
                        through the edge. (default: None)
  -es [edgeId [edgeId ...]], --edge-speed [edgeId [edgeId ...]]
                        Parameter responsible for the extraction of
                        information on the average speed of vehicles that
                        passed through the edge. (default: None)
  -eh [edgeId [edgeId ...]], --edge-halting [edgeId [edgeId ...]]
                        Parameter responsible for the extraction of
                        information on the number of vehicles that were at a
                        traffic jam on the edge. (default: None)
  -el [edgeId [edgeId ...]], --edge-length [edgeId [edgeId ...]]
                        Parameter responsible for the extraction of
                        information on the total length of vehicles that were
                        at a traffic jam on the edge. (default: None)

Vehicle group:
  The parameters that define the focus of simulation and extraction data.

  -va [vehicleId [vehicleId ...]], --vehicle-all [vehicleId [vehicleId ...]]
                        Parameter responsible for the extraction of all the
                        information related to the vehicles. (default: None)
  -vd [vehicleId [vehicleId ...]], --vehicle-distance [vehicleId [vehicleId ...]]
                        Parameter responsible for the extraction of
                        information on the travel distance by the vehicles.
                        (default: None)
  -vt [vehicleId [vehicleId ...]], --vehicle-time [vehicleId [vehicleId ...]]
                        Parameter responsible for the extraction of
                        information on the travel time by the vehicles.
                        (default: None)
  -vs [vehicleId [vehicleId ...]], --vehicle-speed [vehicleId [vehicleId ...]]
                        Parameter responsible for the extraction of
                        information on the mean speed of the vehicles.
                        (default: None)
  -vr [vehicleId [vehicleId ...]], --vehicle-route [vehicleId [vehicleId ...]]
                        Parameter responsible for the extraction of
                        information on the route of the vehicles. (default:
                        None)

Traffic Light group:
  The parameters that define the focus of simulation and extraction data.

  -tla [tlsId [tlsId ...]], --tls-all [tlsId [tlsId ...]]
                        Parameter responsible for the extraction of all the
                        information related to the traffic lights. (default:
                        None)
  -tlh [tlsId [tlsId ...]], --tls-halting [tlsId [tlsId ...]]
                        Parameter responsible for the extraction of the
                        information on the number of vehicles stopped at every
                        lane controlled by the traffic lights. (default: None)

HOW TO USE (EXAMPLES)
---------------------

    Consider that the implementation of this program takes into account that an
instance of SUMO simulator is running.

    PERFORMING A DEFAULT EXTRACTION: The line below will generate, as output of
the simulation, a file for each category referred to the edges. The various
types are described in the "COMMANDS SUPPORTED". The extraction will take into
consideration all the edges that exist for the map, and run by <--step-limit> 
time steps. The data in the output files will be separated by a single space
(' ').
        python sumoplot.py --net <net file path> --edge-all

    PERFORMING A MINIMALIST DEFAULT EXTRACTION: Same as above, but with parame
ters in small size.
        python sumoplot.py -n <net file path> -ea
   
    PERFORMING A PARTIAL EXTRACTION IDENTICAL: The line below will generate, as
output of the simulation, a file for each category "halting vehicles" and
"vehicles that have passed". More information about each type can be seen in
"COMMANDS SUPPORTED". The extraction will take into consideration all the edges
that had their id's past, and run by <--step-limit> time steps. The data in the 
output files will be separated by a single space(' ').
        python sumoplot.py --net <net file path>    \
            --edge-halting <edgeId1 edgeId2 edgeId3> \
            --edge-vehicle <edgeId1 edgeId2 edgeId3>

    PERFORMING A PARTIAL EXTRACTION NOT IDENTICAL: The line below will generate,
as output of the simulation, a file for each category: "halting vehicles" and
"vehicles that have passed". More information about each type can be seen in
"COMMANDS SUPPORTED". The extraction will consider for the first case, all edges
of the map, and the second all the edges that had their id's past, and run by
<--step-limit> time steps. The data in the output files will be separated by a 
single space(' ').
        python sumoplot.py --net <net file path>    \
            --edge-halting  \
            --edge-vehicle <edgeId2 edgeId3>

    MODIFYING THE OUTPUT APPEARANCE: The line below will generate, as output of
the simulation, a file for the category "vehicles mean speed that have passed".
More information about each type can be seen in "COMMANDS SUPPORTED". The extrac
tion will take into consideration all the edges of the map, and run by 
<--step-limit> time steps. The data in the output files will be separated by a 
comma(',').
        python sumoplot.py --net <net file path> --edge-speed --separator <comma>

    DELIMITING THE SCOPE OF ITERATIONS: The line below will generate, as output
of the simulation, a file for the category "jam length of the vehicles that have
stopped". More information about each type can be seen in "COMMANDS SUPPORTED".
The extraction will take into consideration all the edges that had their id's
past, and run for 500 time steps, and exit only take into account the space con
tained between <--step-start> 100 and <--step-end> 400. The data in the output 
files will be separated by an tab('\t').
        python sumoplot.py --net <net file path>    \
            --step-limit <500> --step-start <100> --step-end <400>   \
            --edge-length <edgeId1 edgeId2 edgeId3>     \
            --separator <tab>

    PERFORMING A VEHICLE SPEED EXTRACTION: The line below will generate, as out
put of the simulation, a file for category: "vehicles mean speed". More informa
tion about each type can be seen in "COMMANDS SUPPORTED". The extraction will 
consider all the vehicles that had their id's past.
        python sumoplot.py --net <net file path> \
            --vehicle-speed <vehicleId1 vehicleId2>

    PERFORMING A TRAFFIC LIGHTS EXTRACTION: The line below will generate, as out
put of the simulation, a file for category: "traffic lights halting vehicles". 
More information about each type can be seen in "COMMANDS SUPPORTED". The extrac
tion will consider all the traffic lights that had their id's past.
        python sumoplot.py --net <net file path> \
            --tls-halting <tlsId1 tlsId2>

    PERFORMING A MULTI-OBSERVER EXTRACTION: The line below will generate, as out
put of the simulation, a file for each category: "distance traveled by vehicles" 
and "jam length of the vehicles that have stopped". More information about each 
type can be seen in "COMMANDS SUPPORTED". The extraction will consider for the 
first case, all the vehicles that had their id's past, and the second all the 
edges that had their id's past.
        python sumoplot.py --net <net file path> \
            -vd <vehicleId1 vehicleId2> \
            --edge-length <edgeId1 edgeId2 edgeId3>

    For full information, call in the command shell:
        python sumoplot.py --help
