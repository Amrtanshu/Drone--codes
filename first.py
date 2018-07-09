from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import numpy as np
from pyquaternion import Quaternion
import argparse


# Parse the arguments  

#vehicle = connect(/dev/ttyAMA0,baud=57600 wait_ready=True)
vehicle = connect('127.0.0.1:14550', wait_ready=True)


    
def arm():
     
     print "Basic pre-arm checks"
    # Don't let the user try to arm until autopilot is ready
     while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)


     print ('Arming motors')
     # Copter should arm in GUIDED mode
     vehicle.mode = VehicleMode("GUIDED_NOGPS")
     vehicle.armed = True 


     # Confirm vehicle armed before attempting to take off
     while not vehicle.armed: 
         print ('Waiting for arming...')
         time.sleep(1)

     
def set_attitude (pitch, roll, yaw, thrust):
    
    yaw = np.radians(yaw)
    pitch = np.radians(pitch)
    roll = np.radians(roll) 
    
    # Now calculate the quaternion in preparation to command the change in attitude
    # q for yaw is rotation about z axis
    qyaw = Quaternion (axis = [0, 0, 1], angle = yaw )
    qpitch = Quaternion (axis = [0, 1, 0], angle = pitch )
    qroll = Quaternion (axis = [1, 0, 0], angle = roll )

    # We have components, now to combine them into one quaternion
    q = qyaw * qpitch * qroll
    a = q.elements
    
    rollRate = (roll * 5)
    yawRate = (yaw * 0.5)
   
    msg = vehicle.message_factory.set_attitude_target_encode(
    0,
    0,                #target system
    0,                #target component
    0b0000000,       #type mask
    [a[0],a[1],a[2],a[3]],        #q
    rollRate,                #body roll rate
    0.5,                #body pitch rate
    yawRate,                #body yaw rate
    thrust)                #thrust
    
    vehicle.send_mavlink(msg)

def height_change(altitude):
    height = vehicle.location.global_relative_frame.alt
    while(1):
        height = vehicle.location.global_relative_frame.alt
        if height > altitude + 0.1:
            thrust = 0.45
        elif height < altitude - 0.1:
            thrust = 0.55
        else:
            thrust = 0.5
            set_attitude(0,0,0,thrust)
            print ('HEIGHT ATTAINED')
            time.sleep(5)
            break
        set_attitude(0,10,0,thrust)
        #print thrust,height

def control(alt):
     current=vehicle.location.global_relative_frame.alt
     print ('TAKING_OFF')
     height_change(alt)
     print ("LANDKING")
     vehicle.mode=VehicleMode("LAND")
     while(vehicle.armed!=False):
          time.sleep(1)
     print ("LANDED")    
     vehicle.close()
arm()
control(5)



