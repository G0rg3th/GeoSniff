# Author: Vu Le

import wx
import matplotlib

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanva

# STATE LOOKUP
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# Panel to hold graphs
class GraphPanelHolder(wx.Panel):
    countries = []
    country_data = []

    states = []
    state_data = []

    ips = []
    ip_data = []

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.country_graph = GraphPanel(self, graph_type="country")
        self.state_graph = GraphPanel(self, graph_type="state")
        self.ip_graph = GraphPanel(self, graph_type="ip")
        sizer.Add(self.country_graph, 1, wx.EXPAND)
        sizer.Add(self.state_graph, 1, wx.EXPAND)
        sizer.Add(self.ip_graph, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def update_graphs(self, country, state, ip):
        self.update_countries(country)
        self.update_states(state)
        self.update_ips(ip)
        self.country_graph.draw()
        self.state_graph.draw()
        self.ip_graph.draw()

    def update_countries(self, country):
        for i in range(len(self.countries)):
            if country == self.countries[i]:
                self.country_data[i] = self.country_data[i] + 1
                return
        self.countries.append(country)
        self.country_data.append(1)

    def update_states(self, state):
        if state in us_state_abbrev:
            state_abbr = us_state_abbrev.get(state)
        else:
            state_abbr = "OTHER"
        for i in range(len(self.states)):
            if state_abbr == self.states[i]:
                self.state_data = self.state_data[i] + 1
                return
        self.states.append(state_abbr)
        self.state_data.append(1)

    def update_ips(self, ip):
        for i in range(len(self.ips)):
            if ip == self.ips[i]:
                ip_data = self.ip_data[i] + 1
                return
        self.ips.append(ip)
        self.ip_data.append(1)


# Individual graph panel
class GraphPanel(wx.Panel):
    def __init__(self, parent, graph_type):
        self.graph_type = graph_type

        wx.Panel.__init__(self, parent)

        self.figure = matplotlib.figure.Figure()
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)

        self.set_size()
        self.draw()

        self._resize_flag = False

        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_idle(self, event):
        if self._resize_flag:
            self._resize_flag = False
            self.set_size()

    def on_size(self, event):
        self._resize_flag = True

    def set_size(self):
        pixels = tuple(self.GetSize())
        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches([float(x) / self.figure.get_dpi() for x in pixels])

    def draw(self):
        self.figure.clf()
        ax = self.figure.gca()
        if (self.graph_type == "country"):
            ax.pie(GraphPanelHolder.country_data,  labels=GraphPanelHolder.countries,
                   autopct='%1.1f%%', shadow=True, startangle=90)
        elif (self.graph_type == "state"):
            ax.pie(GraphPanelHolder.state_data, labels=GraphPanelHolder.states,
                   autopct='%1.1f%%', shadow=True, startangle=90)
        elif (self.graph_type == "ip"):
            ax.pie(GraphPanelHolder.ip_data, labels=GraphPanelHolder.ips,
                   autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')
        self.canvas.draw()
