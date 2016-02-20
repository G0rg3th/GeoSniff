#!/usr/bin/env python

try:
    from pyslip.tkinter_error import tkinter_error
except ImportError:
    print('*'*60 + '\nSorry, you must install pySlip first\n' + '*'*60)
    raise
try:
    import wx
except ImportError:
    msg = 'Sorry, you must install wxPython'
    tkinter_error(msg)

import pyslip
import pyslip.osm_tiles as tiles

######
# Various demo constants
######

# initial view level and position
InitViewLevel = 5

InitViewPosition = (-91.179, 30.413)

# list of modules containing tile sources
# list of (<long_name>, <module_name>)
# the <long_name>s go into the Tileselect menu
TileSources = [
               ('OpenStreetMap tiles', 'pyslip.osm_tiles'),
               ('Stamen Toner tiles', 'pyslip.stmt_tiles'),
               ('Stamen Transport tiles', 'pyslip.stmtr_tiles'),
              ]
DefaultTileset = 'OpenStreetMap tiles'


######
# Various GUI layout constants
######

###############################################################################
# The main application frame
###############################################################################

class AppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='pySlip demo')
        self.Maximize()
        self.SetMinSize((300, 300))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour(wx.WHITE)
        self.panel.ClearBackground()

        # create tile set menu items
        menubar = wx.MenuBar()
        tile_menu = wx.Menu()

        # initialise tileset handling
        self.tile_source = None
        # a dict of "gui_id: (name, module_name, object)" tuples
        self.id2tiledata = {}
        # a dict of "name: gui_id"
        self.name2guiid = {}

        self.default_tileset_name = None
        for (name, module_name) in TileSources:
            new_id = wx.NewId()
            tile_menu.Append(new_id, name, name, wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.onTilesetSelect)
            self.id2tiledata[new_id] = (name, module_name, None)
            self.name2guiid[name] = new_id
            if name == DefaultTileset:
                self.default_tileset_name = name

        if self.default_tileset_name is None:
            raise Exception('Bad DefaultTileset (%s) or TileSources (%s)'
                            % (DefaultTileset, str(TileSources)))

        menubar.Append(tile_menu, "&Tileset")
        self.SetMenuBar(menubar)

        self.tile_source = tiles.Tiles()

        # build the GUI
        self.make_gui(self.panel)

        # do initialisation stuff - all the application stuff
        self.init()

        # finally, set up application window position
        self.Centre()

        # create select event dispatch directory
        self.demo_select_dispatch = {}

        # select the required tileset
        item_id = self.name2guiid[self.default_tileset_name]
        tile_menu.Check(item_id, True)

    def onTilesetSelect(self, event):
        """User selected a tileset from the menu.

        event  the menu select event
        """

        menu_id = event.GetId()
        try:
            (name, module_name, new_tile_obj) = self.id2tiledata[menu_id]
        except KeyError:
            # badly formed self.id2tiledata element
            raise Exception('self.id2tiledata is badly formed:\n%s'
                            % str(self.id2tiledata))

        if new_tile_obj is None:
            # haven't seen this tileset before, import and instantiate
            module_name = self.id2tiledata[menu_id][1]
            exec 'import %s as tiles' % module_name
            new_tile_obj = tiles.Tiles()

            # update the self.id2tiledata element
            self.id2tiledata[menu_id] = (name, module_name, new_tile_obj)

        self.pyslip.ChangeTileset(new_tile_obj)


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
        PointData = [(-91.180337, 30.414316)]
        PointDataColour = '#ff000080'  # semi-transparent

        # define layer ID variables & sub-checkbox state variables
        # For deletion:
        # self.pyslip.DeleteLayer(self.point_layer)
        # self.point_layer = None
        self.point_layer = self.pyslip.AddPointLayer(PointData, colour=PointDataColour, radius=5)

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

if __name__ == '__main__':
    # start wxPython app
    app = wx.App()
    app_frame = AppFrame()
    app_frame.Show()

    app.MainLoop()
