README
-------------------------------
*ReadMe File better formatted when downloaded.*

This code will create an alarm clock to be used to power on a record player to wake me up :)
The code can be used to emit a GPIO signal at a certain time.

To use code: combine all files into the same directory. You may need to change run bash to have the proper directory path to timeht16k33.py

Make sure to connect to the internet before starting code. 
The clock will not update to the correct time unless you are connected to the internet.

Once you run the bash, the pins should be configured and alarm.py should be running.
The hex display should turn on once the script is running.

Button and LED Layout
Button/LED           Pin         Function

Button 1             P2_2        Snooze
Button 2             P2_4        Show Alarm
Button 3             P2_6        Set Hour
Button 4             P2_8        Set Minute
Button 5             P2_10       Alarm Toggle

LED 1                P2_3        Alarm ON/OFF LED

How To Use?
------------------------------
To use the alarm, simultaneously, hold down Button 2 and press either Button 3 or Button 4 to set the hour and minutes respectively.
Once you have the desired time, you can release Button 2 and press Button 5 to turn on the Alarm Clock.
LED 1 should turn on once Button 5 is pressed.

Now, patiently wait for your alarm to go off. Once the alarm is set, the Record Player should start playing. 
To stop the alarm, press Button 1 to snooze. 

Youtube Video of Demo is Here: https://youtu.be/3vX1a-8VKSU
Hackster.io Page Here: https://www.hackster.io/hugoestradaii/record-player-alarm-clock-121bae
