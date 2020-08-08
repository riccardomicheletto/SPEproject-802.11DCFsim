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
        self.phy = phy.Phy(self.env, self.name, self.ether, self.latitude, self.longitude)

    def send(self, destination, length, payload):
        macPkt = macPacket.MacPacket(self.name, destination, length, payload)
        self.env.process(self.phy.send(macPkt))
