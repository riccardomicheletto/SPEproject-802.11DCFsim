# 802.11 Distributed Coordination Function Simulator
## Simulation and Performance Evaluation project

Discrete event simulator for the **802.11 CSMA/CA DCF**. The simulator is written in Python and it leverages on the [Simpy](https://simpy.readthedocs.io/en/latest/) framework.

### Usage
After installing Simpy, to execute the simulator it is sufficient to run the ```main.py``` file. To modify the simulation it is possible to modify any parameter of the ```parameters.py``` file. The simulator, by default, performs the transmission of packets of random size and content, sent to random destinations from each node, using a poisson process with increasing rate. The initial and final rate are editable parameters.

It is possible to modify the main to perform different actions, such as sending individual packets.
