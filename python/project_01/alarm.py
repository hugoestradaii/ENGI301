"""
--------------------------------------------------------------------------
Vinyl Player Alarm
--------------------------------------------------------------------------
License:
Copyright 2021 Hugo Estrada II

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

"""

import signal
import Adafruit_BBIO.GPIO as GPIO
import time
import datetime
import os
import timeht16k33 as HT16K33

# Setup
alarm = 0 # Alarm Flag
alarm_hour = 0 
alarm_minute = 0 
i2c_bus=1
i2c_address=0x70

#InitializeButtons
buttonSnooze= "P2_2"
buttonSetAlarm="P2_4"
buttonHour= "P2_6"  
buttonMinute="P2_8"
buttonAlarmToggle="P2_10"

#Initialize LEDs
LEDalarmOnOff="P2_3" 
LEDtest= "P1_4"

#Initialize Display
display= HT16K33.HT16K33(i2c_bus, i2c_address)

#Set correct functions for buttons and LEDs
GPIO.setup(buttonSnooze, GPIO.IN) 
GPIO.setup(buttonSetAlarm, GPIO.IN)
GPIO.setup(buttonHour, GPIO.IN)
GPIO.setup(buttonMinute, GPIO.IN)
GPIO.setup(buttonAlarmToggle, GPIO.IN)
GPIO.setup(LEDalarmOnOff, GPIO.OUT)
GPIO.setup(LEDtest, GPIO.OUT)


GPIO.output(LEDalarmOnOff, alarm)

#Main method to update Hex Display
def update(): 
    global alarm
    global alarm_hour
    global alarm_minute
    while(1):
        
        #Continually check for correct time
        datetime_hour = datetime.datetime.now().hour - 6 # Adjust for CT
        minute = datetime.datetime.now().minute
        hour = datetime_hour # Adjust for CT
        
        #Adjust for CT
        if datetime_hour < 0:
            datetime_hour = datetime_hour + 24
        if hour < 0:
            hour = hour + 24
        if minute > 57:
            minute = minute - 58
        
        #Check Alarm Toggle and Adding Toggle
        if not GPIO.input(buttonAlarmToggle):
            alarm_toggle(buttonAlarmToggle)
        
        #Turning Alarm on at correct time
        if alarm == 1 and alarm_hour == datetime_hour and alarm_minute == minute:
            alarm_on()
            alarm = 0
            GPIO.output(LEDalarmOnOff, GPIO.LOW)
            
        #Showing Alarm or setting time
        if not GPIO.input(buttonSetAlarm):
            if not GPIO.input(buttonHour):
                set_alarm_hour(buttonHour)
            
            if not GPIO.input(buttonMinute):
                set_alarm_minute(buttonMinute)
            
            set_display(alarm_hour, alarm_minute)
        else:
            set_display(hour, minute)
        
        #Snoozing Alarm
        if not GPIO.input(buttonSnooze):
            GPIO.output(LEDtest, GPIO.LOW)
            alarm=0

def alarm_on():
    GPIO.output(LEDtest, GPIO.HIGH)
    return 0

def alarm_off(channel):
    GPIO.output(LEDtest, GPIO.LOW)
    return 0

#Turn Alarm on or off
def alarm_toggle(channel):
    global alarm
    if alarm == 1:
        alarm = 0
    else:
        alarm = 1
    GPIO.output(LEDalarmOnOff, alarm)

#Setting Alarm Hour
def set_alarm_hour(channel):
    global alarm_hour
    if alarm_hour == 23:
        alarm_hour = 0
    else:
        alarm_hour = alarm_hour + 1

#Setting Alarm minute        
def set_alarm_minute(channel):
    global alarm_minute
    if alarm_minute == 59:
        alarm_minute = 0
    else:
        alarm_minute = alarm_minute + 1

#Write to Display
def set_display(hour, minute):
    
    #Make number into two digits if not already
    if len(str(hour)) == 1:
        hour = str(hour)
        hour = hour.zfill(2)
        
    if len(str(minute)) == 1:
        minute = str(minute)
        minute = minute.zfill(2)
    
    # Set Value to be put onto Display
    value = int(str(hour)+str(minute))
   
    #Update Display 
    display.update(value)
    
    # Turn on Colon
    display.set_colon("enable")              

    # Wait a quarter second
    time.sleep(0.25)
    return 0

#Call the main function
update()