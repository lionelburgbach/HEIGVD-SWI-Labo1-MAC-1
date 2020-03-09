[Livrables](#livrables)

[Échéance](#échéance)

[Quelques pistes importantes](#quelques-pistes-utiles-avant-de-commencer-)

[Travail à réaliser](#travail-à-réaliser)

1. [Deauthentication attack](#1-deauthentication-attack)
2. [Fake channel evil tween attack](#2-fake-channel-evil-tween-attack)
3. [SSID Flood attack](#3-ssid-flood-attack)

# Sécurité des réseaux sans fil

## Laboratoire 802.11 MAC 1

### 1. Deauthentication attack
 
a) Utiliser la fonction de déauthentification de la suite aircrack, capturer les échanges et identifier le Reason code et son interpretation.

**SCREENSHOTS**

__Question__ : quel code est utilisé par aircrack pour déauthentifier un client 802.11. Quelle est son interpretation ?

Code 7:	"Class 3 frame received from nonassociated station"

Les trames de classe 3 sont des trames de 

__Question__ : A l'aide d'un filtre d'affichage, essayer de trouver d'autres trames de déauthentification dans votre capture. Avez-vous en trouvé d'autres ? Si oui, quel code contient-elle et quelle est son interpretation ?

b) Développer un script en Python/Scapy capable de générer et envoyer des trames de déauthentification. Le script donne le choix entre des Reason codes différents (liste ci-après) et doit pouvoir déduire si le message doit être envoyé à la STA ou à l'AP :
* 1 - Unspecified
* 4 - Disassociated due to inactivity
* 5 - Disassociated because AP is unable to handle all currently associated stations
* 8 - Deauthenticated because sending STA is leaving BSS

Chemin du script `/scripts/SWI-Lab-01-Deauth.py`

Utilisation :

```
root@kali:/home/kali/Desktop# python SWI-Lab-Deauth.py --help
usage: SWI-Lab-Deauth.py [-h] -r REASON -b BSSID -s STA [-c COUNT]

802.11 deauth script

optional arguments:
  -h, --help            show this help message and exit
  -r REASON, --reason REASON
                        The 802.11 deauthentification reason code.
  -b BSSID, --BSSID BSSID
                        BSSID
  -s STA, --STA STA     STA
  -c COUNT, --count COUNT
                        Number of packets to send
```

__Question__ : quels codes/raisons justifient l'envoie de la trame à la STA cible et pourquoi ?

* 1 - Unspecified  
Nous n'avons pas trouvé 
* 4 - Disassociated due to inactivity  
Le BSS a détecté que la STA a atteint le temps limite d'inactivité et est par conséquent disassociée du système.
* 5 - Disassociated because AP is unable to handle all currently associated stations  
Le BSS n'arrive plus à supporter la charge actuelle et disassocie la STA pour libérer des ressources.

__Question__ : quels codes/raisons justifient l'envoie de la trame à l'AP et pourquoi ?

* 8 - Deauthenticated because sending STA is leaving BSS  
La STA se déconnecte (à cause de la qualité du signal ou un changement de SSID par exemple) et notifie ainsi le BSS qu'elle quitte le système.

__Question__ : Comment essayer de déauthentifier toutes les STA ?


__Question__ : Quelle est la différence entre le code 3 et le code 8 de la liste ?

Le code 3 est utilisé dans un IBSS ou ESS alors que le code 8 est utilisé pour un BSS.

__Question__ : Expliquer l'effet de cette attaque sur la cible

Le BSS va comprendre que la station à l'intention de quitter la système et va donc invalider sa session. La cible devra s'authentifier à nouveau sur le BSS.

### 2. Fake channel evil tween attack
a)	Développer un script en Python/Scapy avec les fonctionnalités suivantes :

* Dresser une liste des SSID disponibles à proximité
* Présenter à l'utilisateur la liste, avec les numéros de canaux et les puissances
* Permettre à l'utilisateur de choisir le réseau à attaquer
* Générer un beacon concurrent annonçant un réseau sur un canal différent se trouvant à 6 canaux de séparation du réseau original

__Question__ : Expliquer l'effet de cette attaque sur la cible


### 3. SSID flood attack

Développer un script en Python/Scapy capable d'inonder la salle avec des SSID dont le nom correspond à une liste contenue dans un fichier text fournit par un utilisateur. Si l'utilisateur ne possède pas une liste, il peut spécifier le nombre d'AP à générer. Dans ce cas, les SSID seront générés de manière aléatoire.

## Livrables

Un fork du repo original . Puis, un Pull Request contenant :

- Script de Deauthentication de clients 802.11 __abondamment commenté/documenté__

- Script fake chanel __abondamment commenté/documenté__

- Script SSID flood __abondamment commenté/documenté__

- Captures d'écran du fonctionnement de chaque script

-	Réponses aux éventuelles questions posées dans la donnée. Vous répondez aux questions dans votre ```README.md``` ou dans un pdf séparé

-	Envoyer le hash du commit et votre username GitHub par email au professeur et à l'assistant


## Échéance

Le 9 mars 2020 à 23h59
