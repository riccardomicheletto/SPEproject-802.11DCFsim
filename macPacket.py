class MacPacket(object):
    def __init__(self, source, destination, length, id, ack):
        self.source = source
        self.destination = destination
        self.length = length    # in bit
        self.id = id
        self.ack = ack  # bool
