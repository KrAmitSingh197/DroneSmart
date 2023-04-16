## Drone Smart

# Running the world

In Terminal 1
```
roslaunch iq_sim blackhawk.launch 
```
In Terminal 2
```
roscd iq_sim
./blackhawk.sh
OR
bash blackhawk.sh
```
# Running the drones

In Terminal 3
```
cd catkin_ws/src/iq_sim/scripts
python3 takeoff2.py
```
