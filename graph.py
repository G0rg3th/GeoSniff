import threading
import time
import wx
from wx.lib.pubsub import pub
import matplotlib

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

# Authors: Vu Le, Grant Bourque

# STATE ABBREVIATION LOOKUP
us_state_abbrs = {
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


class DrawThread(threading.Thread):
    """Thread class for updating the graphs approximately every 1 second"""

    def __init__(self, panel):
        threading.Thread.__init__(self)
        self.daemon = True
        self.panel = panel

    def run(self):
        while True:
            time.sleep(1)
            wx.CallAfter(self.panel.draw_graphs)


class GraphPanelHolder(wx.Panel):
    """Panel for holding graphs"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.countries = dict()
        self.states = dict()
        self.ips = dict()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.country_graph = GraphPanel(self, graph_type="country")
        self.state_graph = GraphPanel(self, graph_type="state")
        self.ip_graph = GraphPanel(self, graph_type="ip")
        sizer.Add(self.country_graph, 1, wx.EXPAND)
        sizer.Add(self.state_graph, 1, wx.EXPAND)
        sizer.Add(self.ip_graph, 1, wx.EXPAND)

        self.SetSizer(sizer)
        pub.subscribe(self.__onClearData, 'ClearData')

        draw_thread = DrawThread(self)
        draw_thread.start()

    def update_graphs(self, country, state, ip):
        self.increase_country(country)
        self.increase_state(state)
        self.increase_ip(ip)

    def prune_graphs(self, country, state, ip):
        self.decrease_country(country, ip)
        self.decrease_state(state, ip)
        self.delete_ip(ip)

    def draw_graphs(self):
        self.country_graph.draw()
        self.state_graph.draw()
        self.ip_graph.draw()

    def increase_country(self, country):
        if country in self.countries:
            self.countries[country] += 1
        else:
            self.countries[country] = 1

    def decrease_country(self, country, ip):
        self.countries[country] -= self.ips[ip]
        if self.countries[country] == 0:
            del self.countries[country]

    def increase_state(self, state):
        state_abbr = us_state_abbrs.get(state, "OTHER")
        if state_abbr in self.states:
            self.states[state_abbr] += 1
        else:
            self.states[state_abbr] = 1

    def decrease_state(self, state, ip):
        state_abbr = us_state_abbrs.get(state, "OTHER")
        self.states[state_abbr] -= self.ips[ip]
        if self.states[state_abbr] == 0:
            del self.states[state_abbr]

    def increase_ip(self, ip):
        if ip in self.ips:
            self.ips[ip] += 1
        else:
            self.ips[ip] = 1

    def delete_ip(self, ip):
        del self.ips[ip]

    def __onClearData(self):
        self.countries.clear()
        self.states.clear()
        self.ips.clear()
        self.draw_graphs()


class GraphPanel(wx.Panel):
    """Individual graph panel"""

    def __init__(self, parent, graph_type):
        self.graph_type = graph_type

        wx.Panel.__init__(self, parent)

        self.holder = parent

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
        if self.graph_type == "country":
            ax.pie(self.holder.countries.values(), labels=self.holder.countries.keys(),
                   autopct='%1.1f%%', shadow=True, startangle=90)
        elif self.graph_type == "state":
            ax.pie(self.holder.states.values(), labels=self.holder.states.keys(),
                   autopct='%1.1f%%', shadow=True, startangle=90)
        elif self.graph_type == "ip":
            ax.pie(self.holder.ips.values(), labels=self.holder.ips.keys(),
                   autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')
        self.canvas.draw()
