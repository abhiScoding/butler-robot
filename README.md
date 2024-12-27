Type following on terminal to run node

This launches the stage simulator
$ roslaunch test test.launch

This makes robot go to the kitchen
$ rostopic pub -1 chatter std_msgs/String order

This makes robot go to the table
$ rostopic pub -1 chatter std_msgs/String t1
