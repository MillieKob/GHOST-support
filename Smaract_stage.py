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
        Search for available SmarAct sensors and connect to the first one found. Then set the default settings of the first stage in the sensor.
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

        print("MCS2 number of channels: {}.".format(no_of_channels))
        for channel in range(no_of_channels):
            state = ctl.GetProperty_i32(self.d_handle, channel, ctl.Property.CHANNEL_STATE)
            if state & ctl.ChannelState.SENSOR_PRESENT:
                print("MCS2 channel {} has a stage.".format(channel))
            else:
                print("MCS2 channel {} has no stage.".format(channel))

        self.channel = 0 # Select the first stage by default, this can. be changed with connectStage function.
        print("Stage connected")
        
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.REFERENCING_OPTIONS, 0)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, 500000000) # Set the velocity to 500um/s.
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_ACCELERATION, 500000000000)
        
        
    def connectStage(self, channel):
        '''
        Connect to a specific stage and set the default settings of the stage.
        '''
        self.channel = channel
        print("Stage connected")
        
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.REFERENCING_OPTIONS, 0)
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, 500000000) # Set the velocity to 500um/s.
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_ACCELERATION, 500000000000)
        
    def disconnectStage(self):
        '''
        Disconnect the stage and close the handle to the sensor. 
        '''
        ctl.Close(self.d_handle)
        print("Stage/sensor disconnected")
        
    def getState(self): 
        '''
        Returns a binary string which corresponds to the state flags of the channel. The following bits are defined:
        0 - Stage is actively moving
        1 - Stage is in closed loop mode
        2 - Stage is calibrating
        3 - Stage is referencing
        4 - Stage is waiting to power-up before initiating movement
        5 - An integrated sensor is attached to the channel
        6 - Stage is calibrated
        7 - Stage is referenced
        8 - Stage has hit a mechanical stop
        9 - Stage has hit a configured software range limit
        10 - Stage's following error exceeded the configured limit
        11 - Last movement command failed
        12 - Channel is "currently participating in a trajectory stream or performing a waveform movement".
        13 - Stage is overloaded
        14 - Stage is overheated
        15 - State of the electrical reference mark signal
        16 - Channel has valid data for the communication of an electromagnetic positioner
        17 - Positioning fault detected
        18 - Amplifier is enabled on this channel
        19 - Stage is in position
        20 - Break of an electromagnetic driver state
        21 - Tactile sensing is triggered
        For more details look in the MCS2 programmer's guide page 75 
        '''
        self.channel_state=ctl.GetProperty_i32(self.d_handle,self.channel,ctl.Property.CHANNEL_STATE)
        return bin(self.channel_state)[2:]
        
    def getPosition(self):
        '''
        Query the current position of the stage in pm. Return it as an output.
        '''
        position = ctl.GetProperty_i64(self.d_handle,self.channel,ctl.Property.POSITION)
        return position
    
    def setPosition(self, value):
        '''
        Set the position of the stage to a specific value in pm. Input has to be an integer.
        '''
        if value is not int:
            raise TypeError("Input value has to be an integer")
        
        ctl.Move(self.d_handle, self.channel, value)
    
    def stepMove(self,value):
        '''
        Move the stage by the input value in pm. It moves the stage to the sum of its current position and the function input.
        '''
        if value is not int:
            raise TypeError("Input value has to be an integer")
        
        pos=self.getPosition()
        ctl.Move(self.d_handle, self.channel, value+pos)
        
    def setVelocity(self, value):
        '''
        Set the velocity of the stage, the value is in pm/s and has to be an integer.
        '''
        if value is not int:
            raise TypeError("Input value has to be an integer")
        
        ctl.SetProperty_i64(self.d_handle, self.channel, ctl.Property.MOVE_VELOCITY, value)
    
    def calibrate(self):
        '''
        Set the calibration flags to zero (default, page 322) and then callibrate the stage.
        '''
        print("MCS2 start calibration on channel: {}.".format(self.channel))
        ctl.SetProperty_i32(self.d_handle, self.channel, ctl.Property.CALIBRATION_OPTIONS, 0) #Clear all calibration flags before callibrating
        ctl.Calibrate(self.d_handle, self.channel)
        
    def reference(self):
        '''
        Reference the stage.
        '''
        ctl.Reference(self.d_handle, self.channel)
        
    def stop(self):
        '''
        Stop the movement of the stage. Print a message to the console.
        '''
        ctl.Stop(self.d_handle, self.channel)
        print("Stage movement stopped manually")