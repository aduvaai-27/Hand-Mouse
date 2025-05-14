import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui as pg
import time
capture=cv.VideoCapture(0)
handDitector=mp.solutions.hands.Hands()
drawingUtils=mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen_width, screen_height = pg.size()
index_x = index_y = thumb_x = thumb_y = None
click_cooldown = 0
while 1:
    isTrue, frame=capture.read()
    frame=cv.flip(frame,1)
    
    rgb_frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    frame_height,frame_width, _ =frame.shape
    output=handDitector.process(rgb_frame)
    hands=output.multi_hand_landmarks
    if(hands):
        for hand in hands:
            drawingUtils.draw_landmarks(frame, hand)
            landmarks=hand.landmark
            drawingUtils.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
            for id,landmark in enumerate(landmarks):
                x=int(landmark.x*frame_width)
                y=int(landmark.y*frame_height)
                if(id==8):
                    print(x ,y)
                    cv.circle(frame,(x,y),20,(0,255,255),-1)
                    index_x=screen_width/frame_width*x
                    index_y=screen_height/frame_height*y
                    pg.moveTo(index_x,index_y)
                if(id==4):
                    cv.circle(frame,(x,y),20,(0,0,255),-1)
                    thumb_x=screen_width/frame_width*x
                    thumb_y=screen_height/frame_height*y
    if index_y is not None and thumb_y is not None:
        distance=((index_x-thumb_x)**2 +(index_y-thumb_y)**2)**0.5
        ix_screen = int(index_x * frame_width / screen_width)
        iy_screen = int(index_y * frame_height / screen_height)
        tx_screen = int(thumb_x * frame_width / screen_width)
        ty_screen = int(thumb_y * frame_height / screen_height)
        cv.line(frame, (ix_screen, iy_screen), (tx_screen, ty_screen), (255, 255, 0), 2)

        if distance<60 and time.time()>click_cooldown:
            pg.click()
            click_cooldown=time.time()+1
        
            
    cv.imshow('Virtual Mouse',frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    
capture.release()
cv.destroyAllWindows()

    