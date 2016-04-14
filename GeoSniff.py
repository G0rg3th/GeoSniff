#!/usr/bin/env python

# This is the main script to run the project GeoSniff
# Authors: CSC 3380 Group 20

import wx
from main_window import MainWindow
from listener import Listener
from database import Database
from wx.lib.pubsub import pub
import collections


class App(wx.App):
    """wxPython app class that runs the GUI and interacts with the listener and database."""

    def OnInit(self):
        self.frame = MainWindow(parent=None, title='GeoSniff')
        self.frame.Maximize()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        self.database = Database()
        self.points = collections.OrderedDict()
        pub.subscribe(self.__onClearData, 'ClearData')
        return True

    def is_sniffing(self):
        return self.frame.sniffing

    def add_point_to_map(self, longitude, latitude, point_data_colour='#ff000080'):
        return self.frame.pyslip.AddPointLayer([(longitude, latitude)], colour=point_data_colour, radius=5)

    def receive(self, ip):
        if len(self.points) > 9:
            old_point = self.points.popitem(False)
            self.frame.pyslip.DeleteLayer(old_point[1])
            old_location = self.database.get_location(old_point[0])
            self.frame.graphs_panel.prune_graphs(old_location[2], old_location[3], old_point[0])
        location = self.database.get_location(ip)
        if ip not in self.points:
            self.points[ip] = self.add_point_to_map(location[1], location[0])
        self.frame.graphs_panel.update_graphs(location[2], location[3], ip)

    def set_my_ip(self, my_ip):
        location = self.database.get_location(my_ip)
        self.add_point_to_map(location[1], location[0], '#0000ff')
        self.frame.my_ip_view.SetLabel("Your IP address: " + my_ip)

    def __onClearData(self):
        for point_layer in self.points.values():
            self.frame.pyslip.DeleteLayer(point_layer)
        self.points.clear()


###############################################################################

if __name__ == '__main__':
    # Start wxPython app
    app = App()

    # Start listener thread
    listener = Listener(app)
    listener.start()

    app.MainLoop()
