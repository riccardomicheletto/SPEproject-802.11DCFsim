import simpy


class Node(object):
    def __init__(self, env, name, ether, latitude, longitude):
        self.env = env
        self.name = name
        self.ether = ether
        self.latitude = latitude
        self.longitude = longitude

    def send(self, env, payload):
        yield env.timeout(1)
        msg = (self, payload)
        self.ether.put(msg)

    def listen(self, env):
        inChannel = self.ether.getInChannel(self)
        while True:
            msg = yield inChannel.get()
            print('At time %d %s received message %s from %s' % (self.env.now, self.name, msg[1], msg[0].name))
