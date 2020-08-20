import matplotlib.pyplot as plt
import numpy as np
import parameters

class Stats(object):
    def __init__(self):
        self.generatedPacketsTimes = []     # list of timestamps of generated packets
        self.sentPacketsTimes = []  # list of timestamps of sent packets
        self.deliveredPacketsTimes = []    # list of timestamps of delivered packets

    def logGeneratedPacket(self, timestamp):
        self.generatedPacketsTimes.append(timestamp * 1e-9)

    def logSentPacket(self, timestamp):
        self.sentPacketsTimes.append(timestamp * 1e-9)

    def logDeliveredPacket(self, timestamp):
        self.deliveredPacketsTimes.append(timestamp * 1e-9)

    def printGeneratedPacketTimes(self):
        for generatedPacketTime in self.generatedPacketsTimes:
            print (generatedPacketTime)

    def printSentPacketTimes(self):
        for sentPacketTime in self.sentPacketsTimes:
            print (sentPacketTime)

    def printDeliveredPacketTimes(self):
        for deliveredPacketTime in self.deliveredPacketsTimes:
            print (deliveredPacketTime)

    def plotCumulativePackets(self):
        cumulativePackets = [1]
        for i in range(1, len(self.generatedPacketsTimes)):
            cumulativePackets.append(cumulativePackets[i-1] + 1)

        plt.plot(self.generatedPacketsTimes, cumulativePackets, 'r.', label='Generated')
        plt.plot(self.sentPacketsTimes, cumulativePackets, 'bd', label='Sent')
        plt.plot(self.deliveredPacketsTimes, cumulativePackets, 'g,', label='Delivered')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Packets')
        plt.legend()
        plt.savefig('packets.pdf',bbox_inches='tight', dpi=250)

    def plotThroughput(self):
        # plot throughput
        packetsGeneratedEverySecond = []
        packetsDeliveredEverySecond = []
        for i in range(int(parameters.SIM_TIME * 1e-9)):
            packetsGeneratedEverySecond.append(0)
            packetsDeliveredEverySecond.append(0)

        for timestamp in self.generatedPacketsTimes:
            packetsGeneratedEverySecond[int(timestamp)] += 1

        for timestamp in self.deliveredPacketsTimes:
            packetsDeliveredEverySecond[int(timestamp)] += 1

        seconds = np.arange(0, int(parameters.SIM_TIME * 1e-9), 1)

        plt.plot(seconds, packetsGeneratedEverySecond, 'r.', label='Generated')
        plt.plot(seconds, packetsDeliveredEverySecond, 'g,', label='Delivered')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Throughput')
        plt.legend()
        plt.savefig('throughput.pdf',bbox_inches='tight', dpi=250)
