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
        print('Time %d: %s starts transmission of %s' % (self.env.now, self.name, phyPkt.macPkt.id))
        self.ether.transmit(phyPkt, self.latitude, self.longitude, False) # end of packer = False

        yield self.env.timeout(macPkt.length * parameters.BIT_TRANSMISSION_TIME)
        print('Time %d: %s ends transmission of %s' % (self.env.now, self.name, phyPkt.macPkt.id))
        self.ether.transmit(phyPkt, self.latitude, self.longitude, True) # end of packer = False

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
                    self.mac.sensingTimeout.interrupt(endOfPacket) # I use endOfPacket to generate backoff in case of channel that becomes idle
                if phyPkt.power > parameters.RADIO_SENSITIVITY and not phyPkt.corrupted:
                    if not endOfPacket:  # start of packet
                        self.receivingPackets.append(phyPkt)
                    else:   # end of packet
                        if phyPkt in self.receivingPackets:     # in consider is only if I received the begin of the packer, otherwise I ignore it, as it is for sure corrupted
                            self.receivingPackets.remove(phyPkt)
                            sinr = self.computeSinr(phyPkt)
                            if sinr > 1:    # signal greater than noise and inteference
                                self.mac.handleReceivedPacket(phyPkt.macPkt)


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
        return phyPkt.power/(interference + parameters.BASE_NOISE)
