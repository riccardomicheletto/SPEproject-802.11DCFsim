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

    def waitAck(self, macPkt):
        try:
            yield self.env.timeout(parameters.ACK_TIMEOUT)
            # timeout expired, resend
            print('Time %d: %s retransmit %s to %s' % (self.env.now, self.name, macPkt.id, macPkt.destination))
            self.pendingPackets.pop(macPkt.id)
            self.retransmissionCounter[macPkt.id] += 1
            self.isSensing = True
            self.sensingTimeout = self.env.process(self.waitIdleAndSend(macPkt))

        except simpy.Interrupt:
            # ack received
            self.pendingPackets.pop(macPkt.id)
            self.retransmissionCounter.pop(macPkt.id)
            # TODO: log stats for packet delivered

    def waitIdleAndSend(self, macPkt):
        otherOngoingTransmissions = 0
        timeout = parameters.DIFS_DURATION
        backoff = 0
        if self.retransmissionCounter[macPkt.id] != 0:  # add backoff in case of retransmission
            backoff = random.randint(0, min(pow(2,self.retransmissionCounter[macPkt.id]-1)*parameters.CW_MIN, parameters.CW_MAX)-1)
            timeout += backoff

        while True:
            try:
                while timeout > 0:
                    yield self.env.timeout(1)
                    timeout -= 1

                self.isSensing = False

                self.env.process(self.phy.send(macPkt))
                self.pendingPackets[macPkt.id] = self.env.process(self.waitAck(macPkt))
                return
            except simpy.Interrupt as endOfPacket:
                if not endOfPacket.cause:
                    otherOngoingTransmissions += 1
                else:
                    otherOngoingTransmissions = max(0, otherOngoingTransmissions-1)

                if otherOngoingTransmissions == 0:  # resume timeout
                    if backoff == 0:    # need to add backoff, even if this is not a retransmission
                        backoff = random.randint(0, parameters.CW_MIN-1)
                        timeout += backoff
                    elif timeout > backoff: # backoff has not been consumed, new timeout is DIFS + backoff
                        timeout = parameters.DIFS_DURATION + backoff
                    else:   # backoff has been consumed, new timeout is DIFS + remaining backoff
                        backoff = timeout
                        timeout = parameters.DIFS_DURATION + backoff
                continue
