import simpy
import mac


class Node(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude
        self.mac = mac.Mac(self.env, self.name, self.ether, self.latitude, self.longitude)

    def send(self, destination, length, payload):
        print('Time %d: %s sends %s' % (self.env.now, self.name, payload))
        self.mac.send(destination, length, payload)
