import simpy
import mac


class Node(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude
        self.mac = mac.Mac(self.env, self.name, self.ether, self.latitude, self.longitude)

    def send(self, destination, length, payload):
        yield self.env.timeout(1) # NB: without this timeout it does not work
        self.mac.send(destination, length, payload)

    def listen(self, env):
        inChannel = self.ether.getInChannel(self)
        while True:
            phyPkt = yield inChannel.get()
            print('At time %d %s received message %s from %s with power %.15f' % (self.env.now, self.name, phyPkt.macPacket.id, phyPkt.macPacket.source, phyPkt.power))
