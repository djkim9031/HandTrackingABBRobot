# HandTrackingABBRobot
Gesture Recognition, Hand Tracking, REST API communications


My personal project during the lockdown period using an ABB's IRB14000 (or otherwise named as YuMi).



#How to Use
  
  1. Server computer running the python files should be connected to the robot's LAN port (or service port) using an ethernet cable.
  
  2. Robot's controller should have a file similar to the one at robot_program/rapid.mod
  
  3. Run "python main_starter.py 192.168.125.1" on cmd, and start tracking!
  
  -If the robot is not availble, a virtual robot on Robot Studio can be used. In this case, the hostip should be 127.0.0.1
  -Any robot using robotware version 6.x can be controlled. (any prior version doesn't support REST API communication. So, socket communication needs to be used)
  -For the newer robot batch using robotware version 7.x, REST API methods delineated on https://developercenter.robotstudio.com/api/RWS has to be used. Some calling methods may differ.





#Main Functionalities
  
  1. Hand gesture recognition (Palm, ok sign, V sign, pointing index finger)
  
  2. Recognized palm on a vision camera is constantly tracked in real time. The position of the palm is sent using a REST API protocol to the ABB robot for synchronization.
  
  3. V sign is identified as the "open the gripper" signal, which is also sent using the REST API protocol to the ABB robot
  
  4. An index finger pointing upwared is recognized as the "close the gripper" signal, which is sent using the REST API to the ABB robot
  
  5. OK sign starts the execution of a real-time robot tracking.
  
  6. After some palm-tracking fun, a newly issued ok sign is recognized as the end of real-time robot-tracking. The robot starts revisiting the path tracked by the palm.
  
  7. Robot's leanred path points and Gripper Open/Close signals are saved sequentially in .txt format (This requires ABB's Robot Studio), serving as the "taught" motion instruction for the robot.
  
  
  
  
#Training Data and Architectures Used
  
  1. Initially started with Oxford Hand Dataset for training. The recognized hand shape was limited for my purpose using this data. Therefore, I have collected data personally and drew bounding boxes and annotated labels for every picture.
  
  2. Intentionally, pictures of humans posing different hand gestures at 0.2~1.2m distance from a camera (roughly 2.5% ~ 20% of a frame) are collected
  
  3. 1100 of such pictures are collected
  
  4. Trained using YOLOv3 for bounding box and class detection for general human hands at 0.2~1.2m distance from a cam.
  
  5. Then 200 of each hand gesture (out of 4) for training dataset, and 20 of each for validation dataset are collected.
  
  6. These data are trained using the InceptionV3's Imagenet weights
  
  
  
  
#Limitations
  
  1. Recognized gestures are inaccurate at times depending on the background. This can be solved by applying a better data augmentation scheme or simply collecting more data
  
  2. Data latency (delay time between a gesture recognition and the robot's data acquisition) - it is currently in a few ms range. Perhaps using a socket communication could slightly ameliorate the issue.
