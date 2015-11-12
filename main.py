import graphcustom
from numpy import zeros, roll, linspace
from threading import Thread
from time import sleep
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy import config
import visa
config.Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.lang import Builder
Builder.load_file('graphcustom.kv')


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
        self.bool_off = False
        self.device = DeviceControl()
        self.time = linspace(0, 599, 600)
        self.volt = zeros([600])
        self.curr = zeros([600])
        Thread(target=self.get_curr_volt).start()

    def get_curr_volt(self):
        while not self.bool_off:
            if self.device.read('OUTP?') is not None:
                self.ids.device.text = 'Status : ' + self.device.read('*IDN?')
                volt = self.device.read('MEAS:VOLT?')
                curr = self.device.read('MEAS:CURR?')
                if volt is not None:
                    val = "[b]Voltage Measurement [color=#008000]"
                    self.ids.volt_meas.text = val + volt[:5] + "[/color] V[/b]"
                    self.hist_volt(float(volt))
                    self.ids.graph_volt.draw(self.time, self.volt)
                if curr is not None:
                    val = "[b]Current Measurement [color=#008000]"
                    self.ids.curr_meas.text = val + curr[:5] + "[/color] A[/b]"
                    self.hist_curr(float(curr))
                    self.ids.graph_curr.draw(self.time, self.curr)
                if self.device.read('OUTP?') is not None:
                    if int(self.device.read('OUTP?')) == 0:
                        self.disabler(False)
                    else:
                        self.disabler(True)
                sleep(0.5)
            else:
                self.ids.device.text = 'Status : Device not connected.'
                self.device.open()
                sleep(2)
        return 0

    def disabler(self, on_off):
        self.ids.btn_on.disabled = on_off
        self.ids.btn_off.disabled = not on_off
        self.ids.btn_volt.disabled = not on_off
        self.ids.btn_curr.disabled = not on_off

    def on(self):
        self.device.write("OUTP ON")
        self.disabler(True)

    def off(self):
        self.device.write("OUTP OFF")
        self.disabler(False)

    def setVoltage(self):
        volt = float(self.ids.input_volt.text)
        self.device.write("VOLT " + str(volt))

    def setCurrent(self):
        curr = float(self.ids.input_curr.text)
        self.device.write("CURR " + str(curr))

    def hist_volt(self, volt):
        self.volt = roll(self.volt, -1)
        self.volt[-1] = volt

    def hist_curr(self, curr):
        self.curr = roll(self.curr, -1)
        self.curr[-1] = curr


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.root = MainScreen()
        return self.root

    def on_stop(self):
        self.root.bool_off = True
        self.root.device.close()


class DeviceControl(object):
    def __init__(self):
        super().__init__()
        self.instr = None
        self.rm = None
        self.open()

    def open(self):
        self.rm = visa.ResourceManager()
        try:
            rsc = 'USB0::0x0957::0xA807::US14N7308R::INSTR'
            self.instr = self.rm.open_resource(rsc)
        except:
            self.instr = None
            self.rm.close()
            self.rm = None

    def read(self, command):
        if self.instr is not None:
            try:
                data_read = self.instr.query(command)
                return data_read
            except:
                return None

    def write(self, command):
        if self.instr is not None:
            try:
                self.instr.write(command)
                return 0
            except:
                return 1

    def close(self):
        if self.instr is not None:
            self.instr.close()
            self.instr = None
        if self.rm is not None:
            self.rm.close()
            self.rm = None

if __name__ == "__main__":
    app = MainApp()
    app.run()
