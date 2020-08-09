import simpy
import phy
import macPacket
import parameters

class Mac(object):
    def __init__(self, node):
        self.node = node
        self.env = self.node.env
        self.name = self.node.name
        self.ether = self.node.ether
        self.latitude = self.node.latitude
        self.longitude = self.node.longitude
        self.phy = phy.Phy(self)
        self.pendingPackets = []

    def send(self, destination, payloadLength, id):
        length = payloadLength + parameters.MIN_MAC_PKT_LENGTH
        macPkt = macPacket.MacPacket(self.name, destination, length, id, False)
        self.env.process(self.phy.send(macPkt))

    def handleReceivedPacket(self, macPkt):
        if macPkt.destination == self.name and not macPkt.ack:  # send ack to normal packets
            print('Time %d: %s receives packet %s from %s and sends ACK' % (self.env.now, self.name, macPkt.id, macPkt.source))
            ack = macPacket.MacPacket(self.name, macPkt.source, parameters.MIN_MAC_PKT_LENGTH, macPkt.id, True)
            self.env.process(self.phy.send(ack))
            self.node.receive(macPkt.id, macPkt.source)
        elif macPkt.destination == self.name:
            print('Time %d: %s receives ACK %s from %s' % (self.env.now, self.name, macPkt.id, macPkt.source))
