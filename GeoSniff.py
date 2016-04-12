#!/usr/bin/env python

# This is the main script to run the project GeoSniff


try:
    from pyslip.tkinter_error import tkinter_error
except ImportError:
    print('*' * 60 + '\nSorry, you must install pySlip first\n' + '*' * 60)
    raise
try:
    import wx
except ImportError:
    msg = 'Sorry, you must install wxPython'
    tkinter_error(msg)

import IP2Location
import pyslip
import pyslip.stmtr_tiles as tiles

import Graph


######
# Various demo constants - can be removed later
######

# initial view level and position
InitViewLevel = 5

InitViewPosition = (-91.179, 30.413)


######
# Various GUI layout constants
######

###############################################################################
# The main application frame
###############################################################################

class App(wx.App):
    """wxPython app class that runs the GUI."""

    def OnInit(self):
        self.frame = MainWindow(parent=None, title='GeoSniff')
        self.frame.Maximize()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def add_point_to_map(self, longitude, latitude):
        # For deletion:
        # self.point_layer = self.pyslip.AddPointLayer(point_data, colour=point_data_colour, radius=5)
        # self.pyslip.DeleteLayer(self.point_layer)
        # self.point_layer = None

        point_data = [(longitude, latitude)]
        point_data_colour = '#ff000080'  # semi-transparent
        self.frame.pyslip.AddPointLayer(point_data, colour=point_data_colour, radius=5)





class MainWindow(wx.Frame):
    """Window frame to contain the panels for functionality."""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.actionbar_panel = wx.Panel(self)
        temp_label = wx.StaticText(self.actionbar_panel, -1, "Buttons will go here")

        self.split_graph_map = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.actionbar_panel, 0, wx.ALL, 5)
        sizer.Add(self.split_graph_map, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

        # MAKE GRAPHS PANEL
        self.graphs_panel = Graph.GraphPanelHolder(self.split_graph_map)

        # FOR GRAPH TESTING PURPOSES
        data = Database()
        loc = data.get_location("167.96.56.212")
        self.graphs_panel.update_graphs(loc[2], loc[3], "167.96.52.212")
        loc= data.get_location("8.8.8.8")
        self.graphs_panel.update_graphs(loc[2], loc[3], "167.96.52.222")
        loc= data.get_location("210.129.120.46")
        self.graphs_panel.update_graphs(loc[2], loc[3], "210.129.120.46")
        # END GRAPH STUFF

        self.split_graph_map.Initialize(self.graphs_panel)
        self.map_panel = wx.Panel(self.split_graph_map)
        self.map_panel.ClearBackground()

        self.tile_source = tiles.Tiles()

        # build the GUI
        self.make_gui(self.map_panel)

        # do initialisation stuff - all the application stuff
        self.init()

        self.split_graph_map.SplitVertically(self.graphs_panel, self.map_panel)
        self.split_graph_map.SetMinimumPaneSize(300)


    #####
    # Build the GUI
    #####

    def make_gui(self, parent):
        """Create application GUI."""

        # start application layout
        all_display = wx.BoxSizer(wx.HORIZONTAL)
        parent.SetSizer(all_display)

        # put map view in left of horizontal box
        sl_box = self.make_gui_view(parent)
        all_display.Add(sl_box, proportion=1, flag=wx.EXPAND)

        parent.SetSizerAndFit(all_display)

    def make_gui_view(self, parent):
        """Build the map view widget

        parent  reference to the widget parent

        Returns the static box sizer.
        """

        # create gui objects
        sb = wx.StaticBox(parent)
        self.pyslip = pyslip.PySlip(parent, tile_src=self.tile_source)

        # lay out objects
        box = wx.StaticBoxSizer(sb, orient=wx.HORIZONTAL)
        box.Add(self.pyslip, proportion=1, flag=wx.EXPAND)

        return box

    ######
    # Finish initialization of data, etc
    ######

    def init(self):
        # force pyslip initialisation
        self.pyslip.OnSize()

        # set initial view position
        wx.CallAfter(self.final_setup, InitViewLevel, InitViewPosition)

    def final_setup(self, level, position):
        """Perform final setup.

        level     zoom level required
        position  position to be in centre of view

        We do this in a CallAfter() function for those operations that
        must not be done while the GUI is "fluid".
        """

        self.pyslip.GotoLevelAndPosition(level, position)


###############################################################################

# Class for getting data from the database
class Database:
    # Creates a object with IP2Location API
    def __init__(self):
        self.database = IP2Location.IP2Location("IP2LOCATION-LITE-DB11.BIN")

    # Return a list that has Latitude = 0, Longitude = 1, Country = 2, city = 3
    def get_location(self, ip):
        sender = self.database.get_all(ip)
        ret = [sender.latitude, sender.longitude, sender.country_long, sender.region]
        return ret


if __name__ == '__main__':
    # start wxPython app
    app = App()

    data = Database()
    loc = data.get_location("167.96.56.212")

    app.add_point_to_map(loc[1], loc[0])

    app.MainLoop()
