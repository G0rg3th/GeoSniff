from scapy.all import *
import socket
import threading
import wx


# Authors: Patrick Blanchard, Grant Bourque

class Listener(threading.Thread):
    """Thread class that listens for IPV4 packets on all available interfaces
    and strips out the IP address to send to the app for processing.
    """

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.daemon = True
        self.app = app
        self.ip = socket.gethostbyname(socket.gethostname())
        wx.CallAfter(self.app.set_my_ip, self.ip)

    def run(self):
        while True:
            while self.app.is_sniffing():
                pkt = sniff(filter="ip", count=1)
                ip_src = pkt[0][1].src
                if ip_src != self.ip:
                    wx.CallAfter(self.app.receive, ip_src)
