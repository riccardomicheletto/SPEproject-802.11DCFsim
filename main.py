import simpy
import random

import node
import phy
import ether
import parameters
import stats

def main():
    random.seed(parameters.RANDOM_SEED)
    env = simpy.Environment()
    eth = ether.Ether(env)
    statistics = stats.Stats()

    nodes = []

    for i in range(0, parameters.NUMBER_OF_NODES):
        name = "Node" + str(i)
        nodes.append(node.Node(env, name, eth, random.randint(0,40), random.randint(0,40), statistics))

    for i in range(0, parameters.NUMBER_OF_NODES):
        destinations = []
        for j in range(0, parameters.NUMBER_OF_NODES):
            if i != j:
                destinations.append(nodes[j].name)
        env.process(nodes[i].keepSending(parameters.STARTING_RATE, parameters.TARGET_RATE, destinations))

    if not parameters.PRINT_LOGS:
        env.process(printProgress(env))

    env.run(until=parameters.SIM_TIME)

    statistics.plotCumulativePackets()
    statistics.plotThroughput()
    statistics.plotDelays()
    statistics.plotRetransmissions()

def printProgress(env):
    while True:
        print('Progress: %d / %d' % (env.now * 1e-9, parameters.SIM_TIME * 1e-9))
        yield env.timeout(1e9)

if __name__ == '__main__':
    main()
