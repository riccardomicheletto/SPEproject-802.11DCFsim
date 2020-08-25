import matplotlib.pyplot as plt
import numpy as np
import parameters

class Stats(object):
    def __init__(self):
        self.generatedPacketsTimes = []     # list of timestamps of generated packets
        self.deliveredPacketsTimes = []    # list of timestamps of delivered packets

    def logGeneratedPacket(self, timestamp):
        self.generatedPacketsTimes.append(timestamp * 1e-9)

    def logDeliveredPacket(self, timestamp):
        self.deliveredPacketsTimes.append(timestamp * 1e-9)

    def printGeneratedPacketTimes(self):
        for generatedPacketTime in self.generatedPacketsTimes:
            print (generatedPacketTime)

    def printDeliveredPacketTimes(self):
        for deliveredPacketTime in self.deliveredPacketsTimes:
            print (deliveredPacketTime)

    def plotCumulativePackets(self):
        plt.figure(1)

        cumulativeGeneratedPackets = [1]
        for i in range(1, len(self.generatedPacketsTimes)):
            cumulativeGeneratedPackets.append(cumulativeGeneratedPackets[i-1] + 1)

        cumulativeDeliveredPackets = [1]
        for i in range(1, len(self.deliveredPacketsTimes)):
            cumulativeDeliveredPackets.append(cumulativeDeliveredPackets[i-1] + 1)

        plt.plot(self.generatedPacketsTimes, cumulativeGeneratedPackets, 'r:', label='Generated')
        plt.plot(self.deliveredPacketsTimes, cumulativeDeliveredPackets, 'g:', label='Delivered')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Packets')
        plt.legend()
        plt.savefig('results/packets.pdf',bbox_inches='tight', dpi=250)

    def plotThroughput(self):
        plt.figure(2)
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

        plt.plot(seconds, packetsGeneratedEverySecond, 'r:', label='Generated')
        plt.plot(seconds, packetsDeliveredEverySecond, 'g:', label='Delivered')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Throughput')
        plt.legend()
        plt.savefig('results/throughput.pdf',bbox_inches='tight', dpi=250)
