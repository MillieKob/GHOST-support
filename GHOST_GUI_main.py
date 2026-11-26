import numpy as np

from GUI import Ui_MainWindow
from Smaract_stage import Stage
from ZHI import ZurichInstruments

class GHOST_GUI():
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.stage = Stage()
        self.lockin = ZurichInstruments()