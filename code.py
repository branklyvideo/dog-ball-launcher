# import all the stuff you need

import time
import random

import board
import busio
import pwmio

import digitalio
# sensor & servo
import adafruit_vl53l0x
from adafruit_motor import servo

sensor_on = digitalio.DigitalInOut(board.GP2)
sensor_on.direction = digitalio.Direction.OUTPUT
sensor_on.value = True

#pwm for the motor speed
pwm1 = pwmio.PWMOut(board.GP15, frequency=5000, duty_cycle=0)
pwm2 = pwmio.PWMOut(board.GP14, frequency=5000, duty_cycle=0)

#output for the motor direction setup
motor1_1 = digitalio.DigitalInOut(board.GP11)
motor1_2 = digitalio.DigitalInOut(board.GP12)

motor2_1 = digitalio.DigitalInOut(board.GP13)
motor2_2 = digitalio.DigitalInOut(board.GP10)

motor1_1.direction = digitalio.Direction.OUTPUT
motor1_2.direction = digitalio.Direction.OUTPUT
motor2_1.direction = digitalio.Direction.OUTPUT
motor2_2.direction = digitalio.Direction.OUTPUT

motor1_1.value = True
motor1_2.value = False
motor2_1.value = False
motor2_2.value = True

pwm1.duty_cycle = 0
pwm2.duty_cycle = 0

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.GP1, board.GP0)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#servo init
pwm = pwmio.PWMOut(board.GP16, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)

# set servo to close
my_servo.angle = 180
time.sleep(0.5)

# loop 
while True:
    # sensor checks if the ball is there
    if (vl53.range < 50):
        #random number for the motor speed
        motor_power = random.randrange(40000, 64000, 2000)
        print(motor_power)
        #random wait to make it more fun
        time.sleep(random.randrange(0, 3, 1))
        
        pwm1.duty_cycle = motor_power
        #short pause to reduce amps during motor start up
        time.sleep(0.5)
        pwm2.duty_cycle = motor_power 
        #wait 2 seconds till motors are on full speed
        time.sleep(2)
        #release the ball
        my_servo.angle = 120
        print("Trigger")
        #wait one second
        time.sleep(1.0)
        #stop motors
        pwm1.duty_cycle = 0 
        pwm2.duty_cycle = 0
        #reset servo to closed position
        my_servo.angle = 180
        time.sleep(1)
    
    

