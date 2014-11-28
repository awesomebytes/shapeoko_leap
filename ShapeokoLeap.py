#!/usr/bin/python
################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from lib.grblstuff import setup_logging, hello_grbl, do_command
from lib.getch import getch


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Getting CNC..."
        self.grbl = hello_grbl("/dev/ttyACM0", None)
        print "Got CNC!"
        print "Setting absolute mode"
        do_command(self.grbl, "G90")
        print "Done."
        print "Setting speeds"
        do_command(self.grbl, "$4=2000.000")
        do_command(self.grbl, "$5=2000.000")
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def adapt_num(self, num):
        num = num / 10.0 # CNC works with centimeters in X and Y?
        min_val = -220.0 # To limit in case it wants to go way too far
        max_val = 220.0
        if num > max_val:
            num = max_val
        if num < min_val:
            num = min_val
        return num

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)
            
            x = float(hand.palm_position[0]) # X
            x = self.adapt_num(x)
            y = float(hand.palm_position[2]) # Y
            y = self.adapt_num(y) * -1.0 # our axis is flipped
            
            z = float(hand.palm_position[1]) # Z
            if z < 300.0: # under 30cm we draw
                z = 0.0
            else:
                z = 4.0
            command = "G00 X" + str(x) + " Y" + str(y) + " Z" + str(z)
            print "Sending command: " + command
            do_command(self.grbl, command)#, wait=False)


            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
#             print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
#                 direction.pitch * Leap.RAD_TO_DEG,
#                 normal.roll * Leap.RAD_TO_DEG,
#                 direction.yaw * Leap.RAD_TO_DEG)



        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
