#!/usr/bin/env python3
# Import ROS.
import rospy
# Import the API.
from source import *
# To print colours (optional).
from PrintColours import *
import numpy as np

# drone_coords = np.loadtxt("drone_coords.txt", delimiter=",")
def load_goals_from_file(file_path):
    goals = []
    with open(file_path) as f:
        for line in f:
            # Split each line into x, y, z, and psi values
            x, y, z, psi = line.strip().split(',')
            goals.append([float(x), float(y), float(z), float(psi)])
    return goals
def main():
    # Initializing ROS node.
    rospy.init_node("drone_controller", anonymous=True)
    drones=[]
    # # Create an object for the API.
    # drone = gnc_api()
    # # Wait for FCU connection.
    # drone.wait4connect()
    # # Wait for the mode to be switched.
    # drone.wait4start()
    #
    # # Create local reference frame.
    # drone.initialize_local_frame()
    # # Request takeoff with an altitude of 3m.
    # drone.takeoff(3)
    for i in range(12):
        drone = gnc_api()
        drone.wait4connect()
        drone.wait4start()
        drone.initialize_local_frame()
        drone.takeoff(3)
        drones.append(drone)
    # Specify control loop rate. We recommend a low frequency to not over load the FCU with messages. Too many messages will cause the drone to be sluggish.
    rate = rospy.Rate(3)
    goals = load_goals_from_file('goals.txt')
    # Specify some waypoints
    # goals = [(drone_coords[i][0], drone_coords[i][1], drone_coords[i][2], drone_coords[i][3]) for i in range(12)]
    i = 0

    while i < len(goals):
        for drone in drones:
            drone.set_destination(
            x=goals[i][0], y=goals[i][1], z=goals[i][2], psi=goals[i][3])
        rate.sleep()
        reached=[drone.check_waypoint_reached() for drones in drone]
        if all(reached):
            i += 1
    # Land after all waypoints is reached
    for drone in drones:
        drone.land()
    rospy.loginfo(CGREEN2 + "All waypoints reached landing now." + CEND)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
