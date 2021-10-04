'''
Name: cleaner_bot_controller.py
Author: Chandravaran Kunjeti
'''

import time
import RPi.GPIO as GPIO
import sys, select, termios, tty

'''
Class that contains all the function required to control the robot.
'''
class CleanerBotControl:
    def __init__(self):
        '''
        Looking at the robot from the back the naming convention is given.
        '''
        self.motor_left_in1  = 24  # Pin for the left motor positive terminal
        self.motor_left_in2  = 23  # Pin for the left motor negative terminal
        self.motor_left_en   = 25  # Pin to enable the left motor
        self.motor_right_in1 = 4   # Pin for the right motor positive terminal
        self.motor_right_in2 = 27  # Pin for the right motor negative terminal
        self.motor_right_en  = 22  # Pin to enable the right motor

        self.servo1_left_pin  = 19 # PWM pin of the left front motor-servo
        self.servo2_right_pin = 26 # PWM pin of the right front motor-servo
        self.servo3_flap_pin  = 21 # PWM pin of the flap motor-servo

        self.fan_motor_pin = 12 # Trigger pin for the PC Fan.

        self.count = 1 # Varriable to reprint the options.

        # Setting Mode
        GPIO.setmode(GPIO.BCM)

        # Setup
        GPIO.setup(self.motor_right_in1,GPIO.OUT)
        GPIO.setup(self.motor_right_in2,GPIO.OUT)
        GPIO.setup(self.motor_right_en,GPIO.OUT)

        GPIO.setup(self.motor_left_in1,GPIO.OUT)
        GPIO.setup(self.motor_left_in2,GPIO.OUT)
        GPIO.setup(self.motor_left_en,GPIO.OUT)

        GPIO.setup(self.servo1_left_pin,GPIO.OUT)
        GPIO.setup(self.servo2_right_pin,GPIO.OUT)
        GPIO.setup(self.servo3_flap_pin,GPIO.OUT)

        GPIO.setup(self.fan_motor_pin,GPIO.OUT)

        # Initialization
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.LOW)

        GPIO.output(self.fan_motor_pin,GPIO.LOW)

        # Setting up pdm on enable pin
        self.motor_right=GPIO.PWM(self.motor_right_en,1000)
        self.motor_left=GPIO.PWM(self.motor_left_en,1000)

        self.servo1 = GPIO.PWM(self.servo1_left_pin,50)
        self.servo2 = GPIO.PWM(self.servo2_right_pin,50)
        self.servo3 = GPIO.PWM(self.servo3_flap_pin,50)

        self.duty_cycle_right = 40
        self.duty_cycle_left  = 40

        # Keeping low speed
        self.motor_right.start(self.duty_cycle_right)
        self.motor_left.start(self.duty_cycle_left)
        self.servo1.start(0)
        self.servo2.start(0)
        self.servo3.start(0)

        self.msg = """

        This code allows us teleoperation control of cleaner bot.

        The input is a keyboard press, with the following options

        ---------------------------
        Moving around:
        u    i    o
        j    k    l
        m    ,    .
        anything else : stop
        1 : Low
        2 : Medium
        3 : High

        c: Closing the front arms
        v: Opening the front arms

        d: Closing the front flap
        f: opening the front flap

        r: Fan on
        t: Fan on

        CTRL-C to quit
        ---------------------------
        """

        print(self.msg)

        self.main()

    '''
    Brief: The Function to move forward.
    '''
    def moveForward(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.HIGH)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.HIGH)
        GPIO.output(self.motor_left_in2,GPIO.LOW)

        print("Forward")

    '''
    Brief: The Function to stop the robot.
    '''
    def stop(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.LOW)

        print("Stop")

    '''
    Brief: The Function to move backward.
    '''
    def moveBackward(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.HIGH)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.HIGH)
        print("Backward")

    '''
    Brief: The Function to turn left in place.
    '''
    def turnLeftInPlace(self):

        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.HIGH)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.HIGH)
        print("Turn left in place")

    '''
    Brief: The Function to turn right in place.
    '''
    def turnRightInPlace(self):

        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.HIGH)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.HIGH)
        GPIO.output(self.motor_left_in2,GPIO.LOW)
        print("Turn right in place")

    '''
    Brief: The Function to turn left about left wheel while moving forward.
    '''
    def turnLeftAboutLeftWheelFront(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.HIGH)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.LOW)
        print("Turn left about left wheel front")

    '''
    Brief: The Function to turn right about right wheel while moving forward.
    '''
    def turnRightAboutRightWheelFront(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.HIGH)
        GPIO.output(self.motor_left_in2,GPIO.LOW)
        print("Turn right about right wheel front")

    '''
    Brief: The Function to turn left about left wheel while moving backward.
    '''
    def turnLeftAboutLeftWheelBack(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.HIGH)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.LOW)
        print("Turn left about left wheel back")

    '''
    Brief: The Function to turn right about right wheel while moving backward.
    '''
    def turnRightAboutRightWheelBack(self):
        # Right Motor
        GPIO.output(self.motor_right_in1,GPIO.LOW)
        GPIO.output(self.motor_right_in2,GPIO.LOW)

        # Left Motor
        GPIO.output(self.motor_left_in1,GPIO.LOW)
        GPIO.output(self.motor_left_in2,GPIO.HIGH)

        print("Turn right about right wheel back")

    '''
    Brief: The Function to close the front arms, as the servo in use is a 360* servo
    so it uses velocities to move. As there is no proper relation for between the speed
    of revolution and direction. I am commanding one servo to move for a longer period of
    time.
    '''
    def closeFront(self):
        self.servo1.ChangeDutyCycle(11)
        self.servo2.ChangeDutyCycle(6)
        time.sleep(0.25)
        self.servo1.ChangeDutyCycle(1)
        time.sleep(0.2)
        self.servo2.ChangeDutyCycle(1)

    '''
    Brief: The Function to open the front arms, as the servo in use is a 360* servo
    so it uses velocities to move. As there is no proper relation for between the speed
    of revolution and direction. I am commanding one servo to move for a longer period of
    time.
    '''
    def openFront(self):
        self.servo1.ChangeDutyCycle(6)
        self.servo2.ChangeDutyCycle(11)
        time.sleep(0.25)
        self.servo2.ChangeDutyCycle(1)
        time.sleep(0.2)
        self.servo1.ChangeDutyCycle(1)

    '''
    Brief: The Function to close the front flap.
    '''
    def flapUp(self):
        self.servo3.ChangeDutyCycle(0.1)

    '''
    Brief: The Function to open the front flap.
    '''
    def flapDown(self):
        self.servo3.ChangeDutyCycle(11.9)

    '''
    Brief: The Function to switch on the vaccum fan.
    '''
    def fanOn(self):
        GPIO.output(self.fan_motor_pin,GPIO.HIGH)

    '''
    Brief: The Function to switch off the vaccum fan.
    '''
    def fanOff(self):
        GPIO.output(self.fan_motor_pin,GPIO.LOW)

    '''
    Brief: The Function to set the duty cycles for the back wheels, to control the speed.
    '''
    def setDuty(self,right,left):
        self.motor_right.ChangeDutyCycle(right)
        self.motor_left.ChangeDutyCycle(left)
        
    '''
    Brief: The function that takes the keyboard interupt
    '''
    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN,termios.tcgetattr(sys.stdin))
        return key

    '''
    Brief: The main function that takes in keyboard input.
    '''
    def main(self):
        while(1):
            key =self.getKey() #raw_input()

            try:
                if key=='k':
                    self.stop()
                    self.count += 1

                elif key=='i':
                    self.moveForward()
                    key='z'
                    self.count += 1

                elif key==',':
                    self.moveBackward()
                    key='z'
                    self.count += 1

                elif key=='j':
                    self.turnLeftInPlace()
                    key='z'

                elif key=='l':
                    self.turnRightInPlace()
                    key='z'
                    self.count += 1

                elif key=='u':
                    self.turnLeftAboutLeftWheelFront()
                    key='z'
                    self.count += 1

                elif key=='o':
                    self.turnRightAboutRightWheelFront()
                    key='z'
                    self.count += 1

                elif key=='m':
                    self.turnLeftAboutLeftWheelBack()
                    key='z'
                    self.count += 1

                elif key=='.':
                    self.turnRightAboutRightWheelBack()
                    key='z'
                    self.count += 1

                elif key=='1':
                    self.setDuty(40,40)
                    print("Low")
                    key='z'
                    self.count += 1

                elif key=='2':
                    self.setDuty(70,70)
                    print("Medium")
                    key='z'
                    self.count += 1

                elif key=='3':
                    self.setDuty(100,100)
                    print("High")
                    key='z'
                    self.count += 1

                elif key=='c':
                    self.closeFront()
                    self.count += 1
                    print("close")
                    key = 'z'

                elif key=='v':
                    self.openFront()
                    self.count += 1
                    print("open")
                    key = 'z'

                elif key=='f':
                    self.flapUp()
                    self.count += 1
                    print("Close Flap")
                    key = 'z'

                elif key=='d':
                   self.flapDown()
                   self.count += 1
                   print("Open Flap")
                   key = 'z'

                elif key=='r':
                    self.fanOn()
                    self.count += 1
                    print("Fan On")
                    key = 'z'

                elif key=='t':
                   self.fanOff()
                   self.count += 1
                   print("Fan off")
                   key = 'z'

                elif key=='e':
                    GPIO.cleanup()
                    print("GPIO Clean up")
                    break

                if self.count%10 == 0:
                    print(self.msg)

            except Exception as e:
                print(e)

            finally:
               termios.tcsetattr(sys.stdin, termios.TCSADRAIN,termios.tcgetattr(sys.stdin))



if __name__ == "__main__":
    control = CleanerBotControl()
