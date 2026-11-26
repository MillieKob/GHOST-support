import numpy as np

from GUI import Ui_MainWindow
from Smaract_stage import Stage
from ZHI import ZurichInstruments

class GHOST_GUI():
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.stage = Stage()
        self.lockin = ZurichInstruments()

# ========================== STAGE FUNCTIONS ==========================

    def connect_sensor(self):
        '''
        Connect to the Smaract stage. This function sets the default velocity of the stage of 500um/s and selects the stage connected to the first port.
        '''
        self.stage.connectSensor()

    def connect_stage(self, channel):
        '''
        Connect to a specified stage. This function sets the default velocity of the stage of 500um/s.
        '''
        self.stage.connectStage(channel)

    def disconnect_stage(self):
        '''
        Disconnect the SmarAct stage and sensor.
        '''
        self.stage.disconnectStage()