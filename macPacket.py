class MacPacket(object):
    def __init__(self, source, destination, length, id):
        self.source = source
        self.destination = destination
        self.length = length
        self.id = id
