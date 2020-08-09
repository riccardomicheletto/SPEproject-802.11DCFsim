import simpy
import mac

class Node(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude
        self.mac = mac.Mac(self)

    def send(self, destination, length, id):
        print('Time %d: %s sends %s to %s' % (self.env.now, self.name, id, destination))
        self.mac.send(destination, length, id)

    def receive(self, id, source):
        print('Time %d: %s receives %s from %s' % (self.env.now, self.name, id, source))
