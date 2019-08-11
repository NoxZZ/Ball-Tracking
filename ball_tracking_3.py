from collections import deque
from imutils.video import VideoStream
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
import argparse
import cv2
import imutils
import time
import datetime
import numpy as np

pp = np.zeros((420,560,3), np.uint8)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

def draw_line(frame):
    line_img = np.zeros_like(frame)
    cv2.line(line_img, (0, int(4*frame.shape[0]/5)), (int(frame.shape[1]), int(4*frame.shape[0]/5)), (255, 0, 0), 2)    
    cv2.circle(line_img, (430, int(4*frame.shape[0]/5)), 5, (0,255,0),2)
    cv2.circle(line_img, (320, int(4*frame.shape[0]/5)), 5, (0,255,0),2)    
    overlapped = cv2.addWeighted(frame, 0.8, line_img, 1, 1)
    return overlapped 

def draw_pie():
    labels = 'Short', 'Good', 'Full'
    lengths = [int(s) , int(g), int(f)]    
    colour = ['red', 'yellow', 'yellowgreen']
    explode = [0, 0.1, 0]
    
    plt.pie(lengths, explode=explode, labels=labels, colors=colour, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()    
    
    
def draw_traj(u):
    global pp
    if u == 0 :
        cv2.line(pp, (0, int(4*frame.shape[0]/5)), (int(frame.shape[1]), int(4*frame.shape[0]/5)), (72,42,185), 4)
        cv2.line(pp, (0, int(3*frame.shape[0]/5)), (int(frame.shape[1]), int(3*frame.shape[0]/5)), (72,42,185), 4)
        cv2.rectangle(pp, (0, int(4*frame.shape[0]/5)-2), (int(frame.shape[1]), int(3*frame.shape[0]/5)+2), (179, 242, 245), -1)
        cv2.line(pp, (60,int(4*frame.shape[0]/5)),(60,int(3*frame.shape[0]/5)),(255, 255, 255),2)
        cv2.line(pp, (964,int(4*frame.shape[0]/5)),(964,int(3*frame.shape[0]/5)),(255, 255, 255),2)
        cv2.line(pp, (860,int(4*frame.shape[0]/5)),(860,int(3*frame.shape[0]/5)),(0, 255, 0),1)
        cv2.line(pp, (640,int(4*frame.shape[0]/5)),(640,int(3*frame.shape[0]/5)),(0, 255, 0),1)
        
    for i in range(1, len(pts)):
    	if pts[i - 1] is None or pts[i] is None:
    		continue

        cv2.line(pp, pts[i - 1], pts[i], (0, 0, 255), 4)
    cv2.imshow("Trajectories", pp)  

def draw_pitch_map(sh, go, fu):
    img = np.zeros((420,560,3), np.uint8)
    cv2.line(img, (0, int(4*frame.shape[0]/5)), (int(frame.shape[1]), int(4*frame.shape[0]/5)), (72,42,185), 4)
    cv2.line(img, (0, int(3*frame.shape[0]/5)), (int(frame.shape[1]), int(3*frame.shape[0]/5)), (72,42,185), 4)
    cv2.rectangle(img, (0, int(4*frame.shape[0]/5)-2), (int(frame.shape[1]), int(3*frame.shape[0]/5)+2), (179, 242, 245), -1)
    cv2.line(img, (60,int(4*frame.shape[0]/5)),(60,int(3*frame.shape[0]/5)),(255, 255, 255),2)
    cv2.line(img, (500,int(4*frame.shape[0]/5)),(500,int(3*frame.shape[0]/5)),(255, 255, 255),2)
    cv2.line(img, (430,int(4*frame.shape[0]/5)),(430,int(3*frame.shape[0]/5)),(0, 255, 0),1)
    cv2.line(img, (320,int(4*frame.shape[0]/5)),(320,int(3*frame.shape[0]/5)),(0, 255, 0),1)
    
    for i in sh:
        cv2.circle(img,tuple(i),4,(0,0,255),-1)
    for i in go:
        cv2.circle(img,tuple(i),4,(0,0,255),-1)
    for i in fu:
        cv2.circle(img,tuple(i),4,(0,0,255),-1)
    cv2.imshow("Pitch Map", img)
    return 
    
#yellowLower = (28, 40, 90)
#yellowUpper = (34, 255, 255)
greenLower = (29, 50, 80)
greenUpper = (64, 255, 255)
pts = deque(maxlen = args["buffer"])
usingPiCam = True
frameSize = (480, 320)
flag = 0
if not args.get("video", False):
    vs = VideoStream(src = 0, usePiCamera = usingPiCam, resolution = frameSize, framerate = 75).start()
    flag = 1
else:
    vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

a=[]
b=[]
text = "-"
e = 0
f1 = 1
s = 0
g = 0
f = 0
short = deque(maxlen = args["buffer"])
good = deque(maxlen = args["buffer"])
full = deque(maxlen = args["buffer"])
sh = []
go = []
fu = []
u = 0

while True:
    frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame, then we have reached the end of the video
    if frame is None:
        break

	# resize the frame, blur it, and convert it to the HSV color space
    if flag == 1:
        frame = imutils.resize(frame, width = 560)
    else: 
        frame = imutils.resize(frame, width = 560)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform a series of dilations and erosions to remove any small blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
    	c = max(cnts, key=cv2.contourArea)
    	((x, y), radius) = cv2.minEnclosingCircle(c)
    	M = cv2.moments(c)
    	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
    	if radius > 20:

            if f1 == 1:
                e1 = cv2.getTickCount()
                f1 = 0
			# draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            a.append(x)
            b.append(y)
            e = 1
    
    if e == 1:
        e2 = cv2.getTickCount()
        t = (e2 - e1)/cv2.getTickFrequency()
        if t>4:
            l = max(b)
            d = b.index(l)
            if a[d]<= 341:
                print(a[d])
                print("Short Length")
                text = "Short Length"
                cv2.putText(frame, "Length : {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                center1 = (int(a[d]), int(l))
                sh.append(center1)
                f1 = 1
		s+=1
                a = []  
                b = []
                e = 0
            elif a[d]<= 460:
                print(a[d])
                print("Good Length")
                text = "Good Length"
                cv2.putText(frame, "Length : {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                center2 = (int(a[d]), int(l))
                go.append(center2)
                f1 = 1
		g+=1
                a = []
                b = []
                e = 0
            elif a[d]>= 460:
                print(a[d])
                print("Full Length")
                text = "Full Length"
                cv2.putText(frame, "Length : {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                center3 = (int(a[d]), int(l))
                fu.append(center3)
                f1 = 1
		f+=1
                a = []
                b = []
                e = 0
                    
	# update the points queue
    pts.appendleft(center)
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Length : {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
	# loop over the set of tracked points
    for i in range(1, len(pts)):
	# if either of the tracked points are None, ignore them
    	if pts[i - 1] is None or pts[i] is None:
    		continue

		# otherwise, compute the thickness of the line and draw the connecting lines
    	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 4)


    draw_traj(u)
    u = 1
        
    if e == 0 :
        pts.clear()

	# show the frame to our screen
    lined_frame = draw_line(frame)
    cv2.imshow("Frame", lined_frame)
    draw_pitch_map(sh, go ,fu)
    #draw_traj(short, good, full)
    key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
    	break

print('Short: ' , s ,' Good ' , g , ' Full: ' , f )

draw_pie()
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    	vs.stop()

# otherwise, release the camera
else:
	vs.release()
cv2.destroyAllWindows()    