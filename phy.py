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
                #print('Time %d: %s receives signal %s from %s with power %.15f' % (self.env.now, self.name, phyPkt.macPkt.id, phyPkt.macPkt.source, phyPkt.power))
                if self.mac.isSensing:  # interrupt mac if it is sensing for idle channel
                    self.mac.sensingTimeout.interrupt(endOfPacket) # I use endOfPacket to generate backoff in case of channel that becomes idle
                if phyPkt.power > parameters.RADIO_SENSITIVITY and not phyPkt.corrupted:
                    if not endOfPacket:  # start of packet
                        self.receivingPackets.append(phyPkt)
                    else:   # end of packet
                        self.receivingPackets.remove(phyPkt)
                        # TODO compute sinr
                        self.mac.handleReceivedPacket(phyPkt.macPkt)


            except simpy.Interrupt as macPkt:        # listening can be interrupted by a message sending
                self.ether.removeInChannel(inChannel, self)
                yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
                print('Time %d: %s stops listening' % (self.env.now, self.name))

                yield self.env.process(self.encapsulateAndTransmit(macPkt.cause))

                inChannel = self.ether.getInChannel(self)
                yield self.env.timeout(parameters.RADIO_SWITCHING_TIME) # simulate time of radio switching
                print('Time %d: %s starts listening' % (self.env.now, self.name))
