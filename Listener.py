from scapy.all import *
import socket


# @author: Patrick Blanchard
# @description: Listens for ipv4 packets on all available interfaces and
#   strips out the IP address
# @date: April 7, 2016
class Listener:
    HOST = socket.gethostbyname(socket.gethostname())

    @staticmethod
    def start():
        while True:
            pkt = sniff(filter="ip", count=1)
            ip_src = pkt[0][1].src
            if ip_src != Listener.HOST:
                print ip_src
