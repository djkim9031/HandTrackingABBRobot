# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 11:12:29 2020

@author: KRDOKIM13
"""


import cv2
import imutils
import time
from util_funcs import create_classifier, findObjects
from REST_comme_class import methods, mastership_request, reset_pp, set_signal

def detection(hostip):
    mainClassNames =['Hand']
    modelConfig ='yolov3_custom_hand.cfg'
    modelWeights ='yolov3_custom_gesture.weights'

    CLASSIFIER_WEIGHTS_FILE = "gesture_classification_InceptionV3.h5"
    gesture_labels = ['closed','ok','open','palm-tracking']
    gesture_labels = sorted(gesture_labels)

    cap = cv2.VideoCapture(0)
    whT = 320

    net = cv2.dnn.readNetFromDarknet(modelConfig ,modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    layerNames = net.getLayerNames()

    outputNames = [layerNames[i[0] -1] for i in net.getUnconnectedOutLayers()]

    classifier = create_classifier()
    classifier.load_weights(CLASSIFIER_WEIGHTS_FILE)

    try:
        ROB = methods('Default User', 'robotics', hostip)
    
        #First, request a mastership from the robot
        mastership_request(ROB)
    
        #Reset program pointer
        reset_pp(ROB)
        time.sleep(0.5)
        
        #Initialize the following signals to zero
        set_signal(ROB,'diClose',0)
        time.sleep(0.5)
        set_signal(ROB,'diOpen',0)    
      

    except KeyboardInterrupt:
        ROB.close()



    while True:
        _, frame = cap.read()
        frame = imutils.resize(frame ,width=800)

        blob = cv2.dnn.blobFromImage(frame ,scalefactor= 1 /255 ,size=(whT ,whT) ,mean=(0 ,0 ,0) ,swapRB=True ,crop=False)
        net.setInput(blob)
        outputs = net.forward(outputNames)
        
        frame=cv2.flip(frame,1)
        findObjects(outputs ,frame,classifier, ROB, mainClassNames, gesture_labels)

        cv2.imshow('Image' ,frame)
        cv2.waitKey(1)
