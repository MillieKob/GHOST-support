from zhinst.toolkit import Session
import numpy as np

class ZurichInstruments:
    def __init__(self):
        self.session = Session('192.168.178.170', 8004) #Set up the IP and port of the Zurich Instruments device
        self.connect_lockin()

    def connect_lockin(self):
        '''
        Connect to the Zurich Instruments lock-in amplifier and set up the demodulators and boxcars for GHOST and differential measurements.
        '''
        self.device = self.session.connect_device("dev32434")
        
        #Laser rep rate trigger for boxcars
        self.session.devices['dev32434'].demods[0].adcselect(2) #Select trigger 1 as the input of demod1
        self.session.devices['dev32434'].demods[0].oscselect(0) #Select the first oscillator for demod1
        self.session.devices['dev32434'].extrefs[0].demodselect(0) #Select externalref1 as osc1
        self.session.devices['dev32434'].extrefs[0].enable(1)
        self.session.devices['dev32434'].demods[0].harmonic(1) #Do not divide the input frequency
        
        self.session.devices['dev32434'].demods[3].adcselect(2) #Select trigger 1 as the input of demod4
        self.session.devices['dev32434'].demods[3].oscselect(1) #Select the second oscillator for demod4
        self.session.devices['dev32434'].extrefs[1].demodselect(3) #Select extref2 as osc2
        self.session.devices['dev32434'].extrefs[1].enable(1)
        self.session.devices['dev32434'].demods[3].harmonic(4) #Divide laser signal used as trigger input
        
        #Boxcars initial settings
        self.session.devices['dev32434'].boxcars[0].enable(1) #enable boxcars
        self.session.devices['dev32434'].boxcars[0].periods(1) #don't average the boxcar
        self.session.devices['dev32434'].boxcars[0].oscselect(0) #trigger boxcar with the first oscillator
        self.session.devices['dev32434'].boxcars[0].inputselect(0) #select voltage as the boxcars input
        self.session.devices['dev32434'].auxouts[0].outputselect(6) #send boxcars output into aux 1
        
        #GHOST demodulator
        self.session.devices['dev32434'].demods[1].adcselect(4) #Select aux1 as the input to demod2
        self.session.devices['dev32434'].demods[1].oscselect(1) #Trigger with oscillator 2
        self.session.devices['dev32434'].demods[1].harmonic(2) #Times to match the GHOST frequency
        self.session.devices['dev32434'].demods[1].rate(40000)
        
        
        #DIFF demodulator
        self.session.devices['dev32434'].demods[2].adcselect(4) #Same input as GHOST demodulator
        self.session.devices['dev32434'].demods[2].oscselect(1) #Same oscillator as GHOST
        self.session.devices['dev32434'].demods[2].harmonic(1) #No division as oscillator 2 matches pump frequency
        self.session.devices['dev32434'].demods[2].rate(40000)

    def disconnect_lockin(self):
        self.device.demods[1].sample.unsubscribe()
        self.device.demods[2].sample.unsubscribe()
        self.session.disconnect_device("DEV32434")
        
    def set_boxcar_start(self,start):
        self.session.devices['dev32434'].boxcars[0].windowstart(start)
    
    def set_boxcar_width(self,size):
        self.session.devices['dev32434'].boxcars[0].windowsize(size)
        
    def set_lockin_phase(self,demod,phase):
        self.session.devices['dev32434'].demods[demod].phaseshift(phase)
    
    def get_GHOST_data(self): #returns an array with X,Y,R, and theta
        self.device.demods[1].sample.subscribe()
        data = self.session.poll(0.05)
        x = np.mean(data[self.device.demods[1].sample]['x'])
        y = np.mean(data[self.device.demods[1].sample]['y'])
        r = np.sqrt(x*x+y*y)
        phase = np.mean(data[self.device.demods[1].sample]['phase'])
        self.device.demods[1].sample.unsubscribe()
        return (x,y,r,phase)
    
    def get_PP_data(self): #same as GHOST data but simultaneously gets information from both demodulators
        self.device.demods[1].sample.subscribe()
        self.device.demods[2].sample.subscribe()
        data = self.session.poll(0.02)
        # self.device.demods[1].sample.unsubscribe()
        # self.device.demods[2].sample.unsubscribe()
        x1 = np.mean(data[self.device.demods[1].sample]['x'])
        y1 = np.mean(data[self.device.demods[1].sample]['y'])
        r1 = np.sqrt(x1*x1+y1*y1)
        phase1 = np.mean(data[self.device.demods[1].sample]['phase'])
        x2 = np.mean(data[self.device.demods[2].sample]['x'])
        y2 = np.mean(data[self.device.demods[2].sample]['y'])
        r2 = np.sqrt(x2*x2+y2*y2)
        phase2 = np.mean(data[self.device.demods[2].sample]['phase'])
        self.device.demods[1].sample.unsubscribe()
        self.device.demods[2].sample.unsubscribe()
        return (x1,y1,r1,phase1,x2,y2,r2,phase2)
    
    def DAQ_setup(self):
        self.daq_module = self.session.modules.daq
        self.daq_module.device('dev32434')
        self.daq_module.type(0)
        # self.daq_module.duration(0.00000001)
        self.daq_module.grid.cols(256)
        self.daq_module.holdoff.time(0.001)
        self.daq_module.subscribe(self.device.demods[1].sample.x)
        self.daq_module.triggernode('/dev32434/demods/1/sample.TrigIn1')
        
    def DAQ_run(self):
        self.daq_module.execute()
        while not self.daq_module.raw_module.finished():
            pass
        result = self.daq_module.read(raw=False, clk_rate=self.device.clockbase())
        data = np.mean((result[self.device.demods[1].sample.x][0].value[0]))
        self.daq_module.clearhistory(1)
        return data