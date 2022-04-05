from ipaddress import collapse_addresses
from tkinter.tix import IMAGE
import cv2
import mediapipe as mp 
import time 
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()

vol_range = volume.GetVolumeRange()
minvol = vol_range[0]
maxvol = vol_range[1]



cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ctime = 0
ptime = 0

# number = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304]
# volume = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    resualt = hands.process(rgb_image)

    if resualt.multi_hand_landmarks:
        for i in resualt.multi_hand_landmarks:
            
            lm = i.landmark
            h , w , c = image.shape
            cx4, cy4 = int(lm[4].x*w), int(lm[4].y*h)
            cx8, cy8 = int(lm[8].x*w), int(lm[8].y*h)
            midy = (cy8 + cy4) / 2
            cx20, cy20 = int(lm[20].x*w), int(lm[20].y*h)
            cv2.circle(image, (cx4,cy4), 5, (0,255,255), 2)
            cv2.circle(image, (cx8,cy8), 5, (0,255,255), 2)
            cv2.line(image, (cx4,cy4), (cx8,cy8), (255,255,255), 1)
            distance = int(math.hypot(cx8-cx4, cy8-cy4))

            vol = np.interp(distance, [80, 270], [minvol, maxvol])
            volper = np.interp(distance, [80, 270], [0, 100])
            
            # if midy + 40 > cy20 > midy - 40:
            cvol = volume.GetMasterVolumeLevel()
            cv2.putText(image, f'{str(int(volper))}%', (10,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 2)
            volume.SetMasterVolumeLevel(vol, None)
            #     # print(cvol)
            # if cvol - 1 < vol < cvol + 1:
            

                

            # cv2.putText(image, str(id), (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),  2)

            # mpDraw.draw_landmarks(image, i, mpHands.HAND_CONNECTIONS)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(image, str(int(fps)), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 2)

    cv2.imshow('main', image)
    cv2.waitKey(1)