__author__ = 'diana'

import numpy as np
import cv2

cap = cv2.VideoCapture('/data/Diana/rsync_data_node/ethoscope_videos/023aeeee10184bb39b0754e75cef7900/ETHOSCOPE_023/2016-04-29_10-19-45/whole_2016-04-29_10-19-45_023aeeee10184bb39b0754e75cef7900_diana-dam-2-fly-6-etho-23-SD_1280x960@25_00000.mp4')

fgbg = cv2.BackgroundSubtractorMOG2()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()