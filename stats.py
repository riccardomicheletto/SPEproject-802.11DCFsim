import matplotlib.pyplot as plt
import numpy as np

import parameters

class Stats(object):
    def __init__(self):
        self.generatedPacketsTimes = {}     # packet id - timestamp of generation
        self.deliveredPacketsTimes = {}    # packet id - timestamp of delivery
        self.retransmissionTimes = []   # timestamps of retransmissions

    def logGeneratedPacket(self, id, timestamp):
        self.generatedPacketsTimes[id] = timestamp * 1e-9

    def logDeliveredPacket(self, id, timestamp):
        self.deliveredPacketsTimes[id] = timestamp * 1e-9

    def logRetransmission(self, timestamp):
        self.retransmissionTimes.append(timestamp * 1e-9)

    def printGeneratedPacketTimes(self):
        for generatedPacket in self.generatedPacketsTimes:
            print (self.generatedPacketsTimes[generatedPacket])

    def printDeliveredPacketTimes(self):
        for deliveredPacket in self.deliveredPacketsTimes:
            print (self.deliveredPacketsTimes[deliveredPacket])

    def plotCumulativePackets(self):
        plt.figure(1)

        cumulativeGeneratedPackets = [1]
        generatedPacketsTimes = []
        i = 0
        for packet in self.generatedPacketsTimes:
            if i != 0:
                cumulativeGeneratedPackets.append(cumulativeGeneratedPackets[i-1] + 1)
            generatedPacketsTimes.append(self.generatedPacketsTimes[packet])
            i += 1

        cumulativeDeliveredPackets = [1]
        deliveredPacketsTimes = []
        i = 0
        for packet in self.deliveredPacketsTimes:
            if i != 0:
                cumulativeDeliveredPackets.append(cumulativeDeliveredPackets[i-1] + 1)
            deliveredPacketsTimes.append(self.deliveredPacketsTimes[packet])
            i += 1

        plt.plot(generatedPacketsTimes, cumulativeGeneratedPackets, 'r:', label='Generated')
        plt.plot(deliveredPacketsTimes, cumulativeDeliveredPackets, 'g:', label='Delivered')

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

        for packet in self.generatedPacketsTimes:
            packetsGeneratedEverySecond[int(self.generatedPacketsTimes[packet])] += 1

        for packet in self.deliveredPacketsTimes:
            packetsDeliveredEverySecond[int(self.deliveredPacketsTimes[packet])] += 1

        seconds = np.arange(0, int(parameters.SIM_TIME * 1e-9), 1)

        plt.plot(seconds, packetsGeneratedEverySecond, 'r:', label='Generated')
        plt.plot(seconds, packetsDeliveredEverySecond, 'g:', label='Delivered')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Throughput')
        plt.legend()
        plt.savefig('results/throughput.pdf',bbox_inches='tight', dpi=250)

    def plotDelays(self):
        plt.figure(3)
        delays = []
        deliveredPacketsTimes = []

        for packet in self.deliveredPacketsTimes:
            deliveredPacketsTimes.append(self.deliveredPacketsTimes[packet])
            delays.append(self.deliveredPacketsTimes[packet] - self.generatedPacketsTimes[packet])

        plt.plot(deliveredPacketsTimes, delays, 'b:', label='Delays')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Delay')
        plt.legend()
        plt.savefig('results/delays.pdf',bbox_inches='tight', dpi=250)

    def plotRetransmissions(self):
        plt.figure(4)
        retransmissionsEverySecond = []
        for i in range(int(parameters.SIM_TIME * 1e-9)):
            retransmissionsEverySecond.append(0)

        for timestamp in self.retransmissionTimes:
            retransmissionsEverySecond[int(timestamp)] += 1

        seconds = np.arange(0, int(parameters.SIM_TIME * 1e-9), 1)

        plt.plot(seconds, retransmissionsEverySecond, 'r:', label='Retransmissions')

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Retransmissions')
        plt.legend()
        plt.savefig('results/retransmissions.pdf',bbox_inches='tight', dpi=250)
