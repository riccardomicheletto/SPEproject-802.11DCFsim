import simpy
import math
from scipy.constants import c, pi

# NB: sim time are nanoseconds, distances are in meters


frequency = 2400000000 # 2.4 GHz
wavelength = c/frequency


class Ether(object):
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.channels = []
        self.listeningNodes = []

    def computeDistance(self, senderLatitude, senderLongitude, receiverLatitude, receiverLongitude):
        return math.sqrt(pow(senderLatitude - receiverLatitude, 2) + pow(senderLongitude - receiverLongitude, 2))

    def latencyAndAttenuation(self, phyPkt, sourceLatitude, sourceLongitude, destinationChannel, destinationNode):
        distance = self.computeDistance(sourceLatitude, sourceLongitude, destinationNode.latitude, destinationNode.longitude)
        delay = round((distance / c) * pow(10, 9), 0)
        yield self.env.timeout(delay)
        receivingPower = phyPkt.power * pow(wavelength/(4 * pi * distance), 2) # NB. used FSPL propagation model
        phyPkt.power = receivingPower
        return destinationChannel.put(phyPkt)

    def transmit(self, phyPkt, sourceLatitude, sourceLongitude):
        events = [self.env.process(self.latencyAndAttenuation(phyPkt, sourceLatitude, sourceLongitude, destinationChannel, destinationNode)) for destinationChannel, destinationNode in zip(self.channels, self.listeningNodes)]
        return self.env.all_of(events)

    def getInChannel(self, node):
        channel = simpy.Store(self.env, capacity=self.capacity)
        self.channels.append(channel)
        self.listeningNodes.append(node)
        return channel
