import simpy
import node
import phy
import ether
import parameters

def main():
    env = simpy.Environment()
    eth = ether.Ether(env)

    node1 = node.Node(env, "Node 1", eth, 0, 0)
    node2 = node.Node(env, "Node 2", eth, 10, 30)
    node3 = node.Node(env, "Node 3", eth, 2, 3)
    node4 = node.Node(env, "Node 4", eth, 6, 2)

    #env.process(node1.send("Node 3", 8184, "1st MSG"))
    #env.process(node2.send("Node 3", 20, "2nd MSG"))
    #env.process(node3.send("Node 2", 200, "3rd MSG"))

    env.process(node1.keepSending(1000, [node2.name, node3.name, node4.name]))
    env.process(node2.keepSending(1000, [node1.name, node3.name, node4.name]))
    env.process(node3.keepSending(1000, [node1.name, node2.name, node4.name]))
    env.process(node4.keepSending(1000, [node1.name, node2.name, node3.name]))

    env.run(until=parameters.SIM_TIME)


if __name__ == '__main__':
    main()
