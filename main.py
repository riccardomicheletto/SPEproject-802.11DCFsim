import simpy
import node
import phy
import ether
import parameters

def main():
    env = simpy.Environment()
    eth = ether.Ether(env)

    node1 = node.Node(env, "Node 1", eth, 1, 1)
    node2 = node.Node(env, "Node 2", eth, 45, 26)
    node3 = node.Node(env, "Node 3", eth, 2, 3)

    #env.process(node2.start())
    #env.process(node3.start())
    #env.process(node1.send("Node 2", 10, "primo messaggio"))
    node1.send("Node 2", 8, "primo messaggio")
    #yield self.env.timeout(10)
    #env.process(node2.send("Node 3", 10, "secondo messaggio"))

    env.run(until=parameters.SIM_TIME)


if __name__ == '__main__':
    main()
