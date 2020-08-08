import simpy
import phy
import macPacket

class Mac(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude
        self.phy = phy.Phy(self)

    def send(self, destination, length, id):
        macPkt = macPacket.MacPacket(self.name, destination, length, id, False)
        self.env.process(self.phy.send(macPkt))

    def handleReceivedPacket(self, macPkt):
        print('Time %d: %s receives packet %s from %s' % (self.env.now, self.name, macPkt.id, macPkt.source))
