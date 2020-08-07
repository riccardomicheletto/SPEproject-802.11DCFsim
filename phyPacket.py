class PhyPacket(object):
    def __init__(self, power, corrupted, macPacket):
        self.power = power
        self.corrupted = corrupted
        self.macPacket = macPacket
