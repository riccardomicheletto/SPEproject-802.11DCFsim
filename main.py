import simpy
import node
import phy
import ether
import parameters
import stats
import random

def main():
    env = simpy.Environment()
    eth = ether.Ether(env)
    statistics = stats.Stats()

    nodes = []

    for i in range(0, parameters.NUMBER_OF_NODES):
        name = "Node" + str(i)
        nodes.append(node.Node(env, name, eth, random.randint(0,50), random.randint(0,50), statistics))

    for i in range(0, parameters.NUMBER_OF_NODES):
        destinations = []
        for j in range(0, parameters.NUMBER_OF_NODES):
            if i != j:
                destinations.append(nodes[j].name)
        env.process(nodes[i].keepSending(1, 1000, destinations))

    env.run(until=parameters.SIM_TIME)

    #statistics.plotCumulativePackets()
    statistics.plotThroughput()

if __name__ == '__main__':
    main()
