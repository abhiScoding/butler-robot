Type following on terminal to run node

This launches the stage simulator

$ roslaunch test test.launch

This makes the robot serve table 1, 2, and 3 and then return to the home position

$ rostopic pub -1 chatter std_msgs/String Order_T1_T2_T3_Home

This makes the robot serve table 1 and then return to the home position

$ rostopic pub -1 chatter std_msgs/String Order_T1_Home
