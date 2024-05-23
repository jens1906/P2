# Robotteknologi-2.-semester
This repository contains material relating to the project made by Rob-2 group 260. 

# Different folders and their contents
- 3d models [Contains 3d files of fixtures input station and gripper]
- Drawio [Files for flowcharts and block diagrams]
- Robot program [Files used in running the solution]
- Safety [File used for running the safety system]
- Validation [Values calculated using the group's inverse kinematics code and values calculated by RoboDK]
- New P2_MobileRobot.rdk [Filed used to simulate ur5 in RoboDK]

# How to run UR5 phone assembly program
1. Open file "New P2_Mobilerobot.rdk" and with a LAN cable connect your computer to the UR5. \
Connect to the UR5 by pressing "connect" -> "connect robot" that can found in the top left of RoboDK, then set the current IP and Port and press connect.

2. Python installation 3.11.9. \
Libraries math, numpy and robodk is all expected to be installed prior.

3. Locate file "Robot Program"/main.py and run it.\
A GUI should pop op and a wished custom phone configuraiton can be submitted.
 