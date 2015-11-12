from numpy import amin, amax
from kivy.uix.behaviors import ButtonBehavior
from kivy.garden.graph import Graph, MeshLinePlot


class GraphCustom(ButtonBehavior, Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot = MeshLinePlot(color=[0, 0, 0.75, 1])
        self.plot.points = [(0, 0)]
        self.add_plot(self.plot)

    def draw(self, x, y, autozoom=True):
        if autozoom:
            self.ymin = 0
            self.ymax = float(amax(y) + 0.1)
            self.x_ticks_major = 200
            self.y_ticks_major = (self.ymax - self.ymin) / 2
        curve = []
        for i in range(len(x)):
            curve.append((x[i], y[i]))
        self.plot.points = curve

    def on_press(self):
        pass
