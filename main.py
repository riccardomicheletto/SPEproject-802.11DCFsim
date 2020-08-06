import simpy
import node
import phy
import ether

SIM_TIME = 1000;

def main():
    env = simpy.Environment()
    eth = ether.Ether(env)

    node1 = node.Node(env, "Node 1", eth, 1, 1)
    node2 = node.Node(env, "Node 2", eth, 15, 22)
    node3 = node.Node(env, "Node 3", eth, 2, 3)

    env.process(node2.listen(env))
    env.process(node3.listen(env))
    env.process(node1.send(env, "primo messaggio"))

    env.run(until=SIM_TIME)


if __name__ == '__main__':
    main()
