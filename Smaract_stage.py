import sys 
import smaract.ctl as ctl
import time

class Stage:
    
    def __init__(self):
        self.assert_lib_compatibility()
        
    def assert_lib_compatibility(self):
        """
        Checks that the major version numbers of the Python API and the
        loaded shared library are the same to avoid errors due to 
        incompatibilities.
        Raises a RuntimeError if the major version numbers are different.
        """
        vapi = ctl.api_version
        vlib = [int(i) for i in ctl.GetFullVersionString().split('.')]
        if vapi[0] != vlib[0]:
            raise RuntimeError("Incompatible SmarActCTL python api and library version.")

    def connectSensor(self):
        '''
        Search for available SmarAct sensors and connect to the first one found (change if more sensors are used). 
        '''
        buffer = ctl.FindDevices() # Generate a list of sensors connect, should be precisely one
        if len(buffer) == 0:
            print("No devices found")
            raise ConnectionError
        locators = buffer.split("\n")
        self.d_handle = ctl.Open(locators[0]) # This handle is used to refer to the sensor, the first entry is chosen
        self.move_mode = ctl.MoveMode.CL_ABSOLUTE # Set the stage to closed loop and absolute position mode
        print("Sensor module connected")
        no_of_channels = ctl.GetProperty_i32(self.d_handle, 0, ctl.Property.NUMBER_OF_CHANNELS)
        # print("MCS2 number of channels: {}.".format(no_of_channels))
        # for channel in range(no_of_channels):
        #     state = ctl.GetProperty_i32(self.d_handle, channel, ctl.Property.CHANNEL_STATE)
        #     if state & ctl.ChannelState.SENSOR_PRESENT:
        #         print("MCS2 channel {} has a stage.".format(channel))
        #     else:
        #         print("MCS2 channel {} has no stage.".format(channel))
        self.channel = 0 # select the first stage by default (depends on which port the stage is plugged into)
        #int(input("Select the channel: ")) # This variable is used to refer to the stage
        print("Stage connected")
        
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.REFERENCING_OPTIONS, 0)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, 50000000)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_ACCELERATION, 500000000000)
        
        
    def connectStage(self, channel):
        self.channel = channel
        print("Stage connected")
        
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.REFERENCING_OPTIONS, 0)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, 50000000)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_ACCELERATION, 500000000000)
        
    def disconnectStage(self):
        ctl.Close(self.d_handle)
        print("Stage/sensor disconnected")
        
    def getState(self): #Returns a binary string which corresponds to the state flags of the channel
        self.channel_state=ctl.GetProperty_i32(self.d_handle,self.channel,ctl.Property.CHANNEL_STATE)
        return bin(self.channel_state)[2:]
        
    def getPosition(self):
        self.position = ctl.GetProperty_i64(self.d_handle,self.channel,ctl.Property.POSITION)
        return self.position
    
    def setPosition(self, value):
        ctl.Move(self.d_handle, self.channel, value)
    
    def stepMove(self,value):
        pos=self.getPosition()
        ctl.Move(self.d_handle, self.channel, value+pos)
        
    def setVelocity(self, value):
        '''
        Set the velocity of the stage, the value is in pm/s and has to be an integer.
        '''
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, value)
    
    def calibrate(self):
        print("MCS2 start calibration on channel: {}.".format(self.channel))
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.CALIBRATION_OPTIONS, 0)
        ctl.Calibrate(self.d_handle, self.channel)
        
    def reference(self):
        ctl.Reference(self.d_handle, self.channel)
        
    def stop(self):
        '''
        Stop the movement of the stage. Print a message to the console.
        '''
        ctl.Stop(self.d_handle, self.channel)
        print("Stage movement stopped manually")