import matplotlib.pyplot as plt
import numpy as np
from numpy import mean, std
from scipy import misc

import parameters

class Stats(object):
    def __init__(self):
        self.generatedPacketsTimes = {}     # packet id - timestamp of generation
        self.deliveredPacketsTimes = {}    # packet id - timestamp of delivery
        self.retransmissionTimes = []   # timestamps of retransmissions


    def logGeneratedPacket(self, id, timestamp):
        self.generatedPacketsTimes[id] = timestamp


    def logDeliveredPacket(self, id, timestamp):
        self.deliveredPacketsTimes[id] = timestamp


    def logRetransmission(self, timestamp):
        self.retransmissionTimes.append(timestamp)


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
            generatedPacketsTimes.append(self.generatedPacketsTimes[packet] * 1e-9)
            i += 1

        cumulativeDeliveredPackets = [1]
        deliveredPacketsTimes = []
        i = 0
        for packet in self.deliveredPacketsTimes:
            if i != 0:
                cumulativeDeliveredPackets.append(cumulativeDeliveredPackets[i-1] + 1)
            deliveredPacketsTimes.append(self.deliveredPacketsTimes[packet] * 1e-9)
            i += 1

        plt.plot(generatedPacketsTimes, cumulativeGeneratedPackets, 'r:', label='Generated')
        plt.plot(deliveredPacketsTimes, cumulativeDeliveredPackets, 'g:', label='Delivered')

        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Packets')
        plt.legend()
        file = 'results/packets' + str(parameters.TARGET_RATE) + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
        print("Total number of generated packets: {}".format(len(generatedPacketsTimes)))
        print("Total number of delivered packets: {}".format(len(deliveredPacketsTimes)))

    def plotThroughputMs(self):
        plt.figure(2)
        packetsGeneratedEveryMillisecond = []
        packetsDeliveredEveryMillisecond = []
        for i in range(int(parameters.SIM_TIME * 1e-6)):
            packetsGeneratedEveryMillisecond.append(0)
            packetsDeliveredEveryMillisecond.append(0)
    
        for packet in self.generatedPacketsTimes:
            packetsGeneratedEveryMillisecond[int(self.generatedPacketsTimes[packet] * 1e-6)] += 1
    
        for packet in self.deliveredPacketsTimes:
            packetsDeliveredEveryMillisecond[int(self.deliveredPacketsTimes[packet] * 1e-6)] += 1
    
        milliseconds = np.arange(0, int(parameters.SIM_TIME * 1e-6), 1)
    
        plt.plot(milliseconds, packetsGeneratedEveryMillisecond, 'r:', label='Generated')
        plt.plot(milliseconds, packetsDeliveredEveryMillisecond, 'g:', label='Delivered')
        plt.hlines(mean(packetsGeneratedEveryMillisecond), 0, milliseconds[-1], colors='black', label='Generated mean')
        plt.hlines(mean(packetsDeliveredEveryMillisecond), 0, milliseconds[-1], colors='yellow', label='Delivered mean')
    
        plt.legend()
        plt.xlabel('Time (ms)')
        plt.ylabel('Throughput (packets/ms)')
        plt.legend()
        file = 'results/throughput' + str(parameters.TARGET_RATE) + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
        print("Average number of packets genetated every millisecond: {}".format(mean(packetsGeneratedEveryMillisecond)))
        print("Average number of packets delivered every millisecond: {}".format(mean(packetsDeliveredEveryMillisecond)))
        print("Standard deviation of packets genetated every millisecond: {}".format(std(packetsGeneratedEveryMillisecond)))
        print("Standard deviation of packets delivered every millisecond: {}".format(std(packetsDeliveredEveryMillisecond)))
        

    def plotThroughput(self):
        plt.figure(2)
        packetsGeneratedEverySecond = []
        packetsDeliveredEverySecond = []
        for i in range(int(parameters.SIM_TIME * 1e-9)):
            packetsGeneratedEverySecond.append(0)
            packetsDeliveredEverySecond.append(0)
    
        for packet in self.generatedPacketsTimes:
            packetsGeneratedEverySecond[int(self.generatedPacketsTimes[packet] * 1e-9)] += 1
    
        for packet in self.deliveredPacketsTimes:
            packetsDeliveredEverySecond[int(self.deliveredPacketsTimes[packet] * 1e-9)] += 1
    
        seconds = np.arange(0, int(parameters.SIM_TIME * 1e-9), 1)
    
        plt.plot(seconds, packetsGeneratedEverySecond, 'r:', label='Generated')
        plt.plot(seconds, packetsDeliveredEverySecond, 'g:', label='Delivered')
        plt.hlines(mean(packetsGeneratedEverySecond), 0, seconds[-1], colors='black', label='Generated mean')
        plt.hlines(mean(packetsDeliveredEverySecond), 0, seconds[-1], colors='yellow', label='Delivered mean')
    
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (packets/s)')
        plt.legend()
        file = 'results/throughput' + str(parameters.TARGET_RATE) + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
        print("Average number of packets genetated every second: {}".format(mean(packetsGeneratedEverySecond)))
        print("Average number of packets delivered every second: {}".format(mean(packetsDeliveredEverySecond)))
        print("Standard deviation of packets genetated every second: {}".format(std(packetsGeneratedEverySecond)))
        print("Standard deviation of packets delivered every second: {}".format(std(packetsDeliveredEverySecond)))


    def plotDelays(self):
        plt.figure(3)
        delays = []
        deliveredPacketsTimes = []

        for packet in self.deliveredPacketsTimes:
            deliveredPacketsTimes.append(self.deliveredPacketsTimes[packet] * 1e-9)
            delays.append(self.deliveredPacketsTimes[packet] * 1e-6 - self.generatedPacketsTimes[packet] * 1e-6)

        plt.plot(deliveredPacketsTimes, delays, 'b:', label='Delays')
        plt.hlines(mean(delays), 0, deliveredPacketsTimes[-1], colors='red', label='Delays mean')

        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Delay (ms)')
        plt.legend()
        file = 'results/delays' + str(parameters.TARGET_RATE) + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
        print("Average delay: {}".format(mean(delays)))
        print("Standard deviation of delay: {}".format(std(delays)))
        print("Minimum delay: {}".format(min(delays)))
        print("Maximum delay: {}".format(max(delays)))
        


    def plotRetransmissions(self):
        plt.figure(4)
        retransmissionsEveryMillisecond = []
        for i in range(int(parameters.SIM_TIME * 1e-6)):
            retransmissionsEveryMillisecond.append(0)

        cumulative = 0
        for timestamp in self.retransmissionTimes:
            cumulative = cumulative + 1
            retransmissionsEveryMillisecond[int(timestamp * 1e-6)] = cumulative

        for i in range(1, len(retransmissionsEveryMillisecond)):
            if retransmissionsEveryMillisecond[i] == 0:
                retransmissionsEveryMillisecond[i] = retransmissionsEveryMillisecond[i - 1]

        milliseconds = np.arange(0, int(parameters.SIM_TIME * 1e-6), 1)

        plt.plot(milliseconds, retransmissionsEveryMillisecond, 'r:', label='Retransmissions')

        plt.legend()
        plt.xlabel('Time (ms)')
        plt.ylabel('Retransmissions')
        plt.legend()
        file = 'results/retransmissions' + str(parameters.TARGET_RATE) + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
        print("Total number of retransmissions: {}".format(cumulative))
