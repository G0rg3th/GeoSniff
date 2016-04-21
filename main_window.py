import wx
import pyslip
import pyslip.stmtr_tiles as tiles
import graph
from wx.lib.pubsub import pub


# Authors: Grant Bourque, Vu Le

class MainWindow(wx.Frame):
    """Window frame to contain the panels for functionality."""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.panel = wx.Panel(self)

        self.sniffing = True

        self.toggle_button = wx.Button(self.panel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.ToggleSniffing, self.toggle_button)
        self.clear_button = wx.Button(self.panel, -1, "Clear Data")
        self.Bind(wx.EVT_BUTTON, self.ClearData, self.clear_button)
        self.my_ip_view = wx.StaticText(self.panel, -1, "Your IP address: (unknown)")

        actionbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        actionbar_sizer.AddSpacer((25, 20))
        actionbar_sizer.Add(self.toggle_button)
        actionbar_sizer.AddSpacer((20, 20))
        actionbar_sizer.Add(self.clear_button)
        actionbar_sizer.AddStretchSpacer()
        actionbar_sizer.Add(self.my_ip_view)
        actionbar_sizer.AddSpacer((50, 20))

        self.split_graph_map = wx.SplitterWindow(self.panel, style=wx.SP_LIVE_UPDATE)
        self.graphs_panel = graph.GraphPanelHolder(self.split_graph_map)
        self.map_panel = wx.Panel(self.split_graph_map)
        self.map_panel.ClearBackground()
        self.split_graph_map.SplitVertically(self.graphs_panel, self.map_panel)
        self.split_graph_map.SetMinimumPaneSize(400)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(actionbar_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.split_graph_map, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)

        self.make_gui(self.map_panel)
        self.init()

    def ToggleSniffing(self, event):
        if self.sniffing:
            self.toggle_button.SetLabel("Resume")
        else:
            self.toggle_button.SetLabel("Pause")
        self.sniffing = not self.sniffing

    def ClearData(self, event):
        pub.sendMessage('ClearData')

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
        self.pyslip = pyslip.PySlip(parent, tile_src=tiles.Tiles())

        # lay out objects
        box = wx.StaticBoxSizer(sb, orient=wx.HORIZONTAL)
        box.Add(self.pyslip, proportion=1, flag=wx.EXPAND)

        return box

    def init(self):
        # Force pyslip initialisation
        self.pyslip.OnSize()

        # Set initial view position
        wx.CallAfter(self.final_setup, level=4, position=(-98.583, 39.833))

    def final_setup(self, level, position):
        """Perform final setup.

        level     zoom level required
        position  position to be in centre of view

        We do this in a CallAfter() function for those operations that
        must not be done while the GUI is "fluid".
        """
        self.pyslip.GotoLevelAndPosition(level, position)
