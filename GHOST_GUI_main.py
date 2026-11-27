import numpy as np

import PyQt5

from GUI import Ui_MainWindow
from Smaract_stage import Stage, StageWorker
from ZHI import ZurichInstruments

class GHOST_GUI():
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.stage = Stage()
        self.lockin = ZurichInstruments()

# ========================== STAGE FUNCTIONS ==========================

    def start_stage_worker(self):
        '''
        Start the SmarAct stage worker and set up a thread to receive constant position updates which will be displayed in GUI.
        '''
        self.stageThread = PyQt5.QtCore.QThread() # Variable to hold the stage thread
        self.stageWorker = StageWorker(self.stage) # Variable to hold the stage worker
        self.stageWorker.moveToThread(self.stageThread) # Put the worker on the thread

        # Connect the signals from the worker to the GUI functions
        self.stageWorker.started.connect(self.stageWorker.run)
        self.stageWorker.finished.connect(self.stageWorker.stop)
        self.stageWorker.finished.connect(self.stageWorker.deleteLater)


    def connect_sensor(self):
        '''
        Connect to the SmarAct stage. This function sets the default velocity of the stage of 500um/s and selects the stage connected to the first port.
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