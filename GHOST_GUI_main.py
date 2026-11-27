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

    def get_stage_position(self):
        '''
        Returns the current position of the connected SmarAct stage positioner. Output is in micrometers.
        '''
        return self.stage.getPosition()*1e6

    def move_stage(self, value):
        '''
        Move the connected SmarAct stage to the input position. Value is taken in micrometers.
        '''
        self.stage.setPosition(int(value*1e6))