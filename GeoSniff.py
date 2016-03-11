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


class AppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='GeoSniff')
        self.Maximize()
        self.SetMinSize((300, 300))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour(wx.WHITE)
        self.panel.ClearBackground()

        self.tile_source = tiles.Tiles()

        # build the GUI
        self.make_gui(self.panel)

        # do initialisation stuff - all the application stuff
        self.init()

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
        global PointData, PointDataColour

        # create PointData
        # PointData = [(-91.180337, 30.414316)]
        # PointDataColour = '#ff000080'  # semi-transparent

        # define layer ID variables & sub-checkbox state variables
        # For deletion:
        # self.pyslip.DeleteLayer(self.point_layer)
        # self.point_layer = None
        # self.point_layer = self.pyslip.AddPointLayer(PointData, colour=PointDataColour, radius=5)

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

    def addPointToMap(self, longitude, latitude):
        PointData = [(longitude, latitude)]
        PointDataColour = '#ff000080'  # semi-transparent
        self.pyslip.AddPointLayer(PointData, colour=PointDataColour, radius=5)


###############################################################################

# Class for getting data from the database
class Database:
    # Creates a object with IP2Location API
    def __init__(self):
        self.database = IP2Location.IP2Location("IP2LOCATION-LITE-DB11.BIN")

    # Return a list that has Latitude = 0, Longitude = 1, Country = 2, city = 3
    def getLocation(self, ip):
        sender = self.database.get_all(ip)
        ret = [sender.latitude, sender.longitude, sender.country_long, sender.city]
        return ret


if __name__ == '__main__':
    # start wxPython app
    app = wx.App()
    app_frame = AppFrame()
    app_frame.Show()

    data = Database()

    loc = data.getLocation("167.96.56.212")
    app_frame.addPointToMap(loc[1], loc[0])

    app.MainLoop()

