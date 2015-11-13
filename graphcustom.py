from numpy import amin, amax, ceil, log10
from kivy.uix.behaviors import ButtonBehavior
from kivy.garden.graph import Graph, MeshLinePlot
from numba import jit


@jit
def autoscale(n_array, n_ticks):
    n_min = amin(n_array)
    n_max = amax(n_array)
    if n_min == n_max:
        n_min -= 0.05
        n_max += 0.05
    unroundedTickSize = (n_max - n_min) / (n_ticks-1)
    pow10x = pow(10, ceil(log10(unroundedTickSize) - 1))
    roundedTickRange = ceil(unroundedTickSize / pow10x) * pow10x
    lower_lim = roundedTickRange * round(n_min / roundedTickRange)
    upper_lim = roundedTickRange * round(1 + n_max / roundedTickRange)

    return float(lower_lim), float(upper_lim), roundedTickRange


class GraphCustom(ButtonBehavior, Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot = MeshLinePlot(color=[0, 0, 0.75, 1])
        self.plot.points = [(0, 0)]
        self.add_plot(self.plot)

    def draw(self, x, y, autozoom=True):
        if autozoom:
            self.ymin, self.ymax, self.y_ticks_major = autoscale(y, 3)
            self.xmin, self.xmax, self.x_ticks_major = 0, 600, 200
        curve = []
        for i in range(len(x)):
            curve.append((x[i], y[i]))
        self.plot.points = curve

    def on_press(self):
        pass
