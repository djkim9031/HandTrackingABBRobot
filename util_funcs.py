# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:31:11 2020

@author: KRDOKIM13
"""
import cv2
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from REST_comme_class import reset_pp, set_signal, execute, stop, set_val

IMAGE_SIZE=224

def create_classifier():

    core = InceptionV3(input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), include_top=False, weights="imagenet")
    for layer in core.layers:
      layer.trainable = True

    x = core.output
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(50,activation='relu')(x)
    x = tf.keras.layers.Dense(4,activation='softmax')(x)
    model = tf.keras.Model(inputs=[core.input], outputs=[x])

    return model

def classification(img,x,y,w,h,classifier):
    #img_x_max = img.shape[1]
    #img_y_max = img.shape[0]
    if x < 25:
        x = 25
    if y < 25:
        y = 25
    roi = img[y - 25:y + h + 25, x - 25:x + w + 25]
    roi = cv2.resize(roi, (IMAGE_SIZE, IMAGE_SIZE))
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    roi = preprocess_input(np.array(roi, dtype=np.float32))
    roi = np.expand_dims(roi, axis=0)
    predi = classifier.predict(roi)[0]
    return predi


def findObjects(outputs, img, classifier, ROB, mainClassNames, gesture_labels):
    height ,width , _= img.shape
    bbox = []
    confs = []
    class_ids = []

    for output in outputs:
        for detect in output:
            scores = detect[5:]  # The first 5 values are x,y,w,h,confidence - the remainders are scores for 80(or custom number of) classes
            class_id = np.argmax(scores)  # Index for maximum value in the array
            conf = scores[class_id]
            if conf > 0.3:
                cx ,cy = int(detect[0 ] *width) ,int(detect[1 ] *height)
                w ,h = int(detect[2 ] *width), int(detect[3 ] *height)
                x ,y = int(cx - w /2) ,int(cy - h /2)
                bbox.append([img.shape[1]-x-w ,y ,w ,h])
                confs.append(float(conf))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(bbox, confs, 0.5, 0.4)  # Returning indices of bbox to keep

    for i in indices:
        i = i[0]
        box = bbox[i]
        x ,y ,w ,h = box[0] ,box[1] ,box[2] ,box[3]

        predi = classification(img,x,y,w,h,classifier)
        ind = np.argmax(predi)
        
        if gesture_labels[ind]=='ok' and ROB.count==0:
            cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
            cv2.circle(img, (x+w//2,y+h//2), 2, (0,0,255), 2)
            cv2.putText(img, f'{gesture_labels[1]} {int(predi[ind] * 100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)
       
            set_signal(ROB,'diExternal',0)
            
            execute(ROB,'forever')
            ROB.count+=1
            time.sleep(1)
            
        elif (gesture_labels[ind]=='ok' or gesture_labels[ind]=='palm-tracking') and ROB.count>0:
            
            if gesture_labels[ind]=='ok':
                ROB.count_ok+=1
                cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
                cv2.putText(img, f'{gesture_labels[ind]} {int(predi[ind] * 100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)
                if ROB.count_ok>10:
                    #stop motion and send read signal
                    stop(ROB)
                    reset_pp(ROB)
                    time.sleep(0.3)
                    
                    set_signal(ROB,'diExternal',1)
                    time.sleep(0.5)
                    execute(ROB,'once')                 
                    ROB.count_ok=0
                    ROB.count=0
                    ROB.count_closed=0
                    ROB.count_opened=0
                return

            cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
            cv2.circle(img, (x+w//2,y+h//2), 2, (0,0,255), 2)
            cv2.putText(img, f'{gesture_labels[ind]} {int(predi[ind] * 100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)

            a = img.shape[1]//2-x-w//2
            b= img.shape[0]//2-y-h//2
            set_val(ROB,'val_pc',a,b)

        elif gesture_labels[ind]=='closed' and ROB.count>0:
            cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
            cv2.putText(img, f'{gesture_labels[ind]} {int(predi[ind] * 100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)
            ROB.count_closed+=1
       
            if ROB.count_closed>5:
                
                set_signal(ROB,'diClose',1)
                ROB.count_closed=0
                
                time.sleep(0.3)
                set_signal(ROB,'diClose',0)
                
        elif gesture_labels[ind]=='open' and ROB.count>0:
            cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
            cv2.putText(img, f'{gesture_labels[ind]} {int(predi[ind] * 100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)
            ROB.count_opened+=1
       
            if ROB.count_opened>5:
                
                set_signal(ROB,'diOpen',1)
                ROB.count_opened=0
                
                time.sleep(0.3)
                set_signal(ROB,'diOpen',0)

            print(ROB.count_opened)
            
                
            
        else:
            cv2.rectangle(img ,(x ,y) ,(x+w ,y+h) ,(0 ,0 ,255) ,2)
            cv2.putText(img, f'{mainClassNames[class_ids[i]].upper()} {int(confs[i] *100)}%', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0) ,2)

