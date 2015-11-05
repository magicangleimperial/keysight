from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from numpy import sin
from time import sleep
from kivy import config
from kivy.utils import get_color_from_hex as rgb
config.Config.set('input', 'mouse', 'mouse,disable_multitouch')


class FloatInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False

    def insert_text(self, s, undo=False):
        if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return super(FloatInput, self).insert_text(s, from_undo=undo)
        elif s in ['.', ',']:
            if "." not in self.text:
                if s == ',':
                    s = '.'
                return super(FloatInput, self).insert_text(s, from_undo=undo)

    def on_text_validate(self):
        print(float(self.text))


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on(self):
        print('Set On')

    def off(self):
        print('Set Off')

    def setVoltage(self):
        val = "[b]Voltage Measurement [color=#008000]100[/color] V[/b]"
        self.ids.volt_meas.text = val
        print('Set Voltage')

    def setCurrent(self):
        print('Set Current')


class GraphCustom(ButtonBehavior, Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_options = {'color': rgb('#000000'), 'bold': True}
        self.background_color = rgb('f8f8f2')
        self.tick_color = rgb('808080')
        self.border_color = rgb('808080')
        self.xlabel = 'Time (s)'
        self.x_ticks_minor = 5
        self.x_ticks_major = 25
        self.y_ticks_major = 1
        self.y_grid_label = True
        self.x_grid_label = True
        self.padding = 5
        self.x_grid = True
        self.y_grid = True
        self.xmin = -0
        self.xmax = 100
        self.ymin = -1
        self.ymax = 1

        self.plot = MeshLinePlot(color=[0, 0, 0.75, 1])
        self.plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        self.add_plot(self.plot)

    def redraw(self):
        while not self.stop:
            self.i += 0.1
            self.plot.points = [(x, sin(x / 10. + self.i)) for x in range(0, 101)]
            sleep(0.1)
        return 0

    def on_press(self):
        pass


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.root = MainScreen()
        return self.root

    def on_stop(self):
        pass


if __name__ == "__main__":
    app = MainApp()
    app.run()
