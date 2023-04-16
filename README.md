# DroneSmart

## Setting up the workspace
```
cd
mkdir -p catkin_ws/src
cd catkin_ws/src
git clone https://github.com/KrAmitSingh197/DroneSmart.git
cd ..
catkin_make
```

## Environment Setup
```
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Running the world
In Terminal 1

```
roslaunch iq_sim blackhawk.launch 
```
In Terminal 2

```
roscd iq_sim
./blackhawk.sh
```


## Running The Drones
In Terminal 3

```
cd catkin_ws/src/iq_sim/scripts
python3 test.py
```
