import simpy
import phyPacket

transmittingPower = 0.1 # Watt, legal limit in EU for EIRP

class Phy(object):
    def __init__(self, env, ether, latitude, longitude):
        self.env = env
        self.latitude = latitude
        self.longitude = longitude
        self.ether = ether

    def send(self, macPkt):
        phyPkt = phyPacket.PhyPacket(transmittingPower, False, macPkt)
        self.ether.transmit(phyPkt, self.latitude, self.longitude)
