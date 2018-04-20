# CPS Quadrotor
Quadrotor simulation (based on hector_quadrotor) used for a cyber-physical system verification using formal methods

## Setup
* Install [hector_quadrotor](https://github.com/tu-darmstadt-ros-pkg/hector_quadrotor) packages from source
```
$ mkdir ~/cps_ws
$ cd ~/cps_ws
$ wstool init src https://raw.githubusercontent.com/tu-darmstadt-ros-pkg/hector_quadrotor/kinetic-devel/hector_quadrotor.rosinstall
```

* Clone this repository as an additional package
```
$ cd ~/cps_ws/src
$ git clone <repo-url>
```

* Build the catkin workspace
```
$ ~/cps_ws
$ catkin_make
$ source devel/setup.bash
```

## Run
* Launch the simulation using one of the launch files in the launch directory

`$ roslaunch cps_quadrotor test.launch`
`$ roslaunch cps_quadrotor env.launch world-name:=env1.world`

* Run one of the controllers to control the quadrotor

`$ rosrun cps_quadrotor teleop_pose_keyboard.py`

## Configurations
* In order to change the max xy velocity
  * Go to ~/path-to-workspace/src/hector_quadrotor/hector_quadrotor_controllers/params
  * Edit the file "controller.yaml"
  * Change the value of "max_xy" on line 18

