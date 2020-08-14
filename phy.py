import simpy
import phyPacket
import parameters

class Phy(object):
    def __init__(self, mac):
        self.mac = mac
        self.env = self.mac.env
        self.name = self.mac.name
        self.ether = self.mac.ether
        self.latitude = self.mac.latitude
        self.longitude = self.mac.longitude
        self.listen = self.env.process(self.listen())
        self.receivingPackets = []

    def send(self, macPkt):
        self.receivingPackets.clear() # I switch to transmitting mode, so I drop all ongoing receptions
        yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
        self.listen.interrupt(macPkt)

    def encapsulateAndTransmit(self, macPkt):
        phyPkt = phyPacket.PhyPacket(parameters.TRANSMITTING_POWER, False, macPkt) # start of packet
        if macPkt.ack:
            print('Time %d: %s PHY starts transmission of %s ACK' % (self.env.now, self.name, phyPkt.macPkt.id))
        else:
            print('Time %d: %s PHY starts transmission of %s' % (self.env.now, self.name, phyPkt.macPkt.id))
        self.ether.transmit(phyPkt, self.latitude, self.longitude, False) # end of packet = False

        duration = macPkt.length * parameters.BIT_TRANSMISSION_TIME + parameters.PHY_HEADER_LENGTH

        while True:
            if duration < parameters.SLOT_DURATION:
                yield self.env.timeout(duration)    # wait only remaining time
                break
            yield self.env.timeout(parameters.SLOT_DURATION) # send a signal every slot
            self.ether.transmit(phyPkt, self.latitude, self.longitude, False) # end of packet = False
            duration -= parameters.SLOT_DURATION


        if macPkt.ack:
            print('Time %d: %s PHY ends transmission of %s ACK' % (self.env.now, self.name, phyPkt.macPkt.id))
        else:
            print('Time %d: %s PHY ends transmission of %s' % (self.env.now, self.name, phyPkt.macPkt.id))
        self.ether.transmit(phyPkt, self.latitude, self.longitude, True) # end of packet = True

    def listen(self):
        inChannel = self.ether.getInChannel(self)
        yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
        print('Time %d: %s starts listening' % (self.env.now, self.name))

        while True:
            try:
                (phyPkt, endOfPacket) = yield inChannel.get()

                # the signal just received will interfere with other signals I'm receiving (and vice versa)
                for receivingPkt in self.receivingPackets:
                    if receivingPkt != phyPkt:
                        receivingPkt.interferingSignals[phyPkt.macPkt.id] = phyPkt.power
                        phyPkt.interferingSignals[receivingPkt.macPkt.id] = receivingPkt.power

                #print('Time %d: %s receives signal %s from %s with power %.15f' % (self.env.now, self.name, phyPkt.macPkt.id, phyPkt.macPkt.source, phyPkt.power))

                if self.mac.isSensing:  # interrupt mac if it is sensing for idle channel
                    self.mac.sensingTimeout.interrupt() # I use endOfPacket to generate backoff in case of channel that becomes idle
                if phyPkt.power > parameters.RADIO_SENSITIVITY and not phyPkt.corrupted:
                    if not endOfPacket and phyPkt not in self.receivingPackets:  # start of packet
                        self.receivingPackets.append(phyPkt)
                    elif endOfPacket:   # end of packet
                        if phyPkt in self.receivingPackets:     # in consider is only if I received the begin of the packet, otherwise I ignore it, as it is for sure corrupted
                            self.receivingPackets.remove(phyPkt)
                            sinr = self.computeSinr(phyPkt)
                            if sinr > 1:    # signal greater than noise and inteference
                                self.env.process(self.mac.handleReceivedPacket(phyPkt.macPkt))

            except simpy.Interrupt as macPkt:        # listening can be interrupted by a message sending
                self.ether.removeInChannel(inChannel, self)
                yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
                print('Time %d: %s stops listening' % (self.env.now, self.name))

                yield self.env.process(self.encapsulateAndTransmit(macPkt.cause))

                inChannel = self.ether.getInChannel(self)
                yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
                print('Time %d: %s starts listening' % (self.env.now, self.name))

    def computeSinr(self, phyPkt):
        interference = 0
        for interferingSignal in phyPkt.interferingSignals:
            interference += float(phyPkt.interferingSignals[interferingSignal])
        return phyPkt.power/(interference + parameters.NOISE_FLOOR)
