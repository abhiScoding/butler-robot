Type following on terminal to run node

This launches the stage simulator
$ roslaunch test test.launch

This makes robot go to the kitchen
$ rostopic pub -1 chatter std_msgs/String order

This makes robot go to the table1
$ rostopic pub -1 chatter std_msgs/String t1

This makes robot go to the table2
$ rostopic pub -1 chatter std_msgs/String t2

This makes robot go to the table3
$ rostopic pub -1 chatter std_msgs/String t3

This makes robot go to the home position
$ rostopic pub -1 chatter std_msgs/String home
