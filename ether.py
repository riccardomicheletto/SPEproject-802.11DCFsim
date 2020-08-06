import simpy
import math
from scipy.constants import c

# NB: sim time are nanoseconds


class Ether(object):
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.channels = []
        self.listeningNodes = []

    def computePropagationDelay(self, senderLatitude, senderLongitude, receiverLatitude, receiverLongitude):
        distance = math.sqrt(pow(senderLatitude - receiverLatitude, 2) + pow(senderLongitude - receiverLongitude, 2))
        delay = distance / c
        return round(delay * pow(10, 9), 0)

    def latency(self, msg, store, node):
        delay = self.computePropagationDelay(msg[0].latitude, msg[0].longitude, node.latitude, node.longitude)
        yield self.env.timeout(delay)
        return store.put(msg)

    def put(self, msg):
        if not self.channels:
            raise RuntimeError('There are no output channels.')
        events = [self.env.process(self.latency(msg, channel, node)) for channel, node in zip(self.channels, self.listeningNodes)]
        return self.env.all_of(events)

    def getInChannel(self, node):
        channel = simpy.Store(self.env, capacity=self.capacity)
        self.channels.append(channel)
        self.listeningNodes.append(node)
        return channel
