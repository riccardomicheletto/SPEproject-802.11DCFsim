import simpy
import phyPacket

transmittingPower = 0.1 # Watt, legal limit in EU for EIRP
radioSwitchingTime = 1

class Phy(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude
        self.listen = self.env.process(self.listen())

    def send(self, macPkt):
        yield self.env.timeout(radioSwitchingTime) # simulate time of radio switching
        self.listen.interrupt(macPkt)

    def encapsulateAndTransmit(self, macPkt):
        phyPkt = phyPacket.PhyPacket(transmittingPower, False, macPkt)
        print('Time %d: %s transmits %s' % (self.env.now, self.name, phyPkt.macPacket.id))
        self.ether.transmit(phyPkt, self.latitude, self.longitude)

    def listen(self):
        inChannel = self.ether.getInChannel(self)
        yield self.env.timeout(radioSwitchingTime) # simulate time of radio switching
        print('Time %d: %s starts listening' % (self.env.now, self.name))

        while True:
            try:
                phyPkt = yield inChannel.get()
                print('Time %d: %s receives message %s from %s with power %.15f' % (self.env.now, self.name, phyPkt.macPacket.id, phyPkt.macPacket.source, phyPkt.power))
            except simpy.Interrupt as macPkt:        # listening can be interrupted by a message sending
                self.ether.removeInChannel(inChannel, self)
                yield self.env.timeout(radioSwitchingTime) # simulate time of radio switching
                print('Time %d: %s stops listening' % (self.env.now, self.name))

                self.encapsulateAndTransmit(macPkt.cause)

                inChannel = self.ether.getInChannel(self)
                yield self.env.timeout(radioSwitchingTime) # simulate time of radio switching
                print('Time %d: %s starts listening' % (self.env.now, self.name))
