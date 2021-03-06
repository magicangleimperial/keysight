import graphcustom
from numpy import zeros, roll, linspace
from threading import Thread
from time import sleep
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy import config
import visa
config.Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.lang import Builder
Builder.load_file('graphcustom.kv')
# comment

class WarningPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bool_off = False
        self.device = DeviceControl()
        self.time = linspace(0, 599, 600)
        self.volt = zeros([600])
        self.curr = zeros([600])
        self.warnpop = WarningPopup()
        Thread(target=self.get_curr_volt).start()

    def get_curr_volt(self):
        while not self.bool_off:
            if self.device.read('OUTP?') is not None:
                self.disabler_setting(True)
                try:
                    dev_name = self.device.read('*IDN?')
                    self.ids.device.text = 'Status : ' + dev_name
                    volt = float(self.device.read('MEAS:VOLT?')[1:])
                    curr = float(self.device.read('MEAS:CURR?')[1:])
                    val = "[b]Voltage Measurement [color=#008000]"
                    self.ids.volt_meas.text = val + str(volt)
                    self.ids.volt_meas.text += "[/color] V[/b]"
                    self.hist_volt(float(volt))
                    self.ids.graph_volt.draw(self.time, self.volt)
                    val = "[b]Current Measurement [color=#008000]"
                    self.ids.curr_meas.text = val + str(curr)
                    self.ids.curr_meas.text += "[/color] A[/b]"
                    self.hist_curr(float(curr))
                    self.ids.graph_curr.draw(self.time, self.curr)
                    if self.device.read('OUTP?') is not None:
                        if int(self.device.read('OUTP?')) == 0:
                            self.disabler_onoff(False)
                        else:
                            self.disabler_onoff(True)
                except:
                    print('Reading Issues')
                sleep(0.5)
            else:
                self.disabler_onoff(False)
                self.disabler_setting(False)
                self.ids.device.text = 'Status : Device not connected.'
                self.device.open()
                sleep(2)
        return 0

    def disabler_onoff(self, on_off):
        self.ids.btn_on.disabled = on_off
        self.ids.btn_off.disabled = not on_off

    def disabler_setting(self, on_off):
        self.ids.btn_volt.disabled = not on_off
        self.ids.btn_curr.disabled = not on_off

    def on(self):
        self.device.write("OUTP ON")
        self.disabler_onoff(True)

    def off(self):
        self.device.write("OUTP OFF")
        self.disabler_onoff(False)

    def setVoltage(self):
        volt = float(self.ids.input_volt.text)
        if 0 <= volt <= 300:
            self.device.write("VOLT " + str(volt))
        else:
            self.ids.input_curr.text = 'Wrong Value'

    def setCurrent(self):
        curr = float(self.ids.input_curr.text)
        if 0 <= curr <= 5:
            self.device.write("CURR " + str(curr))
        else:
            self.ids.input_curr.text = 'Wrong Value'

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
        self.close()
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
