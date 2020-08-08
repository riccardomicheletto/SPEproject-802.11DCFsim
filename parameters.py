from scipy.constants import c

# NB: sim time are nanoseconds, distances are in meters

### SIMULATION PARAMETERS
SIM_TIME = 1000;

### RADIO PARAMETERS
TRANSMITTING_POWER = 0.1 # Watt, legal limit in EU for EIRP
RADIO_SWITCHING_TIME = 1
RADIO_SENSITIVITY = 1e-12 # power under which signal is not sensed, approximation for QPSK

### SIGNAL PARAMETERS
FREQUENCY = 2400000000 # 2.4 GHz
WAVELENGTH = c/FREQUENCY

### PHY PARAMETERS
BITRATE = 72000000 # 72 Mbit/s, 802.11n 20MHz channels
BIT_TRANSMISSION_TIME = 1/BITRATE * 1e9

### MAC PARAMETERS
SLOT_DURATION = 20000 # 20 microseconds, 802.11n 2.4 GHz
SIFS_DURATION = 10000 # 10 microseconds, 802.11n 2.4 GHz
DIFS_DURATION = SIFS_DURATION + (2 * SLOT_DURATION)
