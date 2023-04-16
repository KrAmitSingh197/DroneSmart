from pymavlink import mavutil
from time import sleep
import time
import sys
import rospy
from std_msgs.msg import String

import numpy as np
import math 
###read file######
with open('test.txt', 'r') as f:
    lines = f.readlines()
    targets = []
    for line in lines:
        lat, lon, alt = line.strip().split(',')
        targets.append((int(lat), int(lon), int(alt)))
        
#####end here####        
num_drones = 12
formation_radius = 10 # meters
reference_lat = 37.4
reference_lon = -122.0
###########
connections = []
for i in range(num_drones):
    connection = mavutil.mavlink_connection('udpin:localhost:{}'.format(14551 + 10*i))
    connections.append(connection)


# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
for connection in connections:
    connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" %
            (connection.target_system, connection.target_component))
    mode = 'GUIDED'
    mode_id = connection.mode_mapping()[mode]
    connection.mav.set_mode_send(connection.target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id)        



for connection in connections:
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)
    sleep(10)
    connection.mav.command_long_send(connection.target_system, connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 3)
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)
    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)



for i, connection in enumerate(connections):
    target = targets[i]
    cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    params = [0, 0, 0, 0, int(target[0]*1e7), int(target[1]*1e7), target[2]]
    # Send the command to the drone
    connection.mav.command_long_send(connection.target_system, connection.target_component,
                                     cmd, 0, 0, 0, 0, 0, *params)
    # Wait for an acknowledgement message from the drone
    msg = None
    while not msg:
        msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    # Check if the acknowledgement was successful
    if msg.command == cmd and msg.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
        print(f"Command {cmd} sent to drone {connection.target_system} {connection.target_component}")
    else:
        print(f"Error sending command {cmd} to drone {connection.target_system} {connection.target_component}: {msg.result}")


    
while msg.relative_alt <2000:
    msg = connection.recv_match(type ="GLOBAL_POSITION_INT",blocking=True)
    print(msg.relative_alt)

#mode = 'STABILIZE'
#mode_id = the_connection.mode_mapping()[mode]
#the_connection.mav.set_mode_send(the_connection.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id)
