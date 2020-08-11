import simpy
import phy
import macPacket
import parameters
import random

class Mac(object):
    def __init__(self, node):
        self.node = node
        self.env = self.node.env
        self.name = self.node.name
        self.ether = self.node.ether
        self.latitude = self.node.latitude
        self.longitude = self.node.longitude
        self.phy = phy.Phy(self)
        self.pendingPackets = {}    # associate packets I'm trying to transmit and timeouts for retransmissions
        self.retransmissionCounter = {}     # associate packets I'm trying to transmit and transmission attempts
        self.isSensing = False

    def send(self, destination, payloadLength, id):
        length = payloadLength + parameters.MIN_MAC_PKT_LENGTH
        macPkt = macPacket.MacPacket(self.name, destination, length, id, False)

        # sensing phase
        self.retransmissionCounter[macPkt.id] = 0
        self.isSensing = True
        self.sensingTimeout = self.env.process(self.waitIdleAndSend(macPkt))

    def handleReceivedPacket(self, macPkt):
        if macPkt.destination == self.name and not macPkt.ack:  # send ack to normal packets
            print('Time %d: %s receives packet %s from %s and sends ACK' % (self.env.now, self.name, macPkt.id, macPkt.source))
            ack = macPacket.MacPacket(self.name, macPkt.source, parameters.MIN_MAC_PKT_LENGTH, macPkt.id, True)
            self.env.process(self.phy.send(ack))
            self.node.receive(macPkt.id, macPkt.source)
        elif macPkt.destination == self.name:
            print('Time %d: %s receives ACK %s from %s' % (self.env.now, self.name, macPkt.id, macPkt.source))
            if macPkt.id in self.pendingPackets:    # packet could not be in pendingPackets if timeout has expired but ack still arrive
                self.pendingPackets[macPkt.id].interrupt()

    def waitAck(self, pktId):
        try:
            yield self.env.timeout(7000)
            # timeout expired, resend
            self.pendingPackets.pop(pktId)
            # TODO: resend
        except simpy.Interrupt:
            # ack received
            self.pendingPackets.pop(pktId)
            # TODO: log stats for packet delivered

    def waitIdleAndSend(self, macPkt):
        timeout = parameters.DIFS_DURATION
        backoff = 0
        while True:
            try:
                if self.retransmissionCounter[macPkt.id] != 0:  # add backoff in case of retransmission
                    backoff = random.randint(0, min(pow(2,self.retransmissionCounter[macPkt.id]-1)*parameters.CW_MIN, parameters.CW_MAX)-1)
                    timeout += backoff

                yield self.env.timeout(timeout)
                self.isSensing = False

                self.env.process(self.phy.send(macPkt))
                self.pendingPackets[macPkt.id] = self.env.process(self.waitAck(macPkt.id))
                return
            except simpy.Interrupt as endOfPacket:
                if endOfPacket.cause:   # this is not a retransmission, but backoff is used
                    self.retransmissionCounter[macPkt.id] = 1
                    # TODO: freeze backoff and then resume it
                continue
