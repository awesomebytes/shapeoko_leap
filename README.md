shapeoko_leap teleoperate your shapeoko CNC with Leap Motion.

====

Using: https://github.com/welch/shapeoko project to move the CNC with Gcode instructions.

Using a modified version of Leap Motion SDK Sample.

Youtube video of it working:

[![Video of shapeoko teleoperated with Leap Motion](http://img.youtube.com/vi/SVvMEYO3BhU/0.jpg)](https://www.youtube.com/watch?v=SVvMEYO3BhU)

====

How to use it:

I used Ubuntu 12.04 64bits. It should work in similar platforms.

First install Leap Motion SDK: https://developer.leapmotion.com/downloads

I extracted the SDK in ~/LeapSDK (/home/MY_UBUNTU_USER/LeapSDK).


I added environment variables for the SDK:

    export PYTHONPATH=~/LeapSDK/lib:~/LeapSDK/lib/x64:$PYTHONPATH
    export LD_LIBRARY_PATH=~/LeapSDK/lib/x64:$LD_LIBRARY_PATH

I needed to add my user to the group that could access the serial port of the CNC. To do that I checked the group of the serial device:

    ll /dev/ttyACM0
    crw--w---- 1 root dialout 4, 0 Nov 27 20:50 /dev/ttyACM0

Doing ```groups``` I saw I was not in the group, to add myself I did:

    sudo usermod -a -G dialout MY_UBUNTU_USER

And I logged out and logged in (necessary in my case).

Before turning on the CNC put it in the center of the area with the tool halfway up. Just in case you need to invert
some axes for your CNC. Also the Leap Motion is supposed to be in front of you so you can read the LEAP text in your direction.

Z axes is 0.0 when starting the connection to the CNC. It goes to 4.0 when you move the hand at more than 300.00mm up from the Leap Motion.

X axes and Y axes take the raw value and apply the function: ```adapt_num``` to divide the values by 10.0 and apply some limits to the commands to send.

Then plug in the Leap Motion, the USB cable from the shapeoko and execute ```ShapeokoLeap.py```. You may need to change your serial port changing the variable: SERIAL_PORT in the file. By default is ```/dev/ttyACM0```.

Use at your own risk.

You can also move the CNC around to test with ```gdraw``` which is [shapeoko python lib exmaple](https://github.com/welch/shapeoko) modified to use
```ASDW``` to move on the plane (like any game) and ```JK``` to go up and down.

====

Thanks to [AESS](http://aess.upc.es/) for the fun of playing with both things!
