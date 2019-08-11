# Ball-Tracking
# Image Processing Using OpenCV Python
This project aims at making a real-time computer vision system that tracks the exact motion of a ball in 3D using multiple cameras. 
This system is implemented using OpenCV. Ball tracking enables virtual replays, new game statistics, analysing gameplay, and
other visualisations, which result in very new ways of experiencing and analysing cricket matches.
The ready acceptance of the system indicates the growing potential for multi-camera based real-time tracking in broadcast applications.
This product is efficient enough that it works on an embedded device mounted with a PyCamera(tested already).

# Project Overview
Image Processing thus provides the instances of occurrences of ball over the entire frames of the video resulting into trajectory of the ball.
The visualizations and statistics obtained from the ball trajectories have been used in forming the pitch map.
Along with this, the pie chart formed provides the frequency of the lengths of pitched balls.
Thus, a bowler’s performance can be analyzed effectively using this system by virtue of:
1) Trajectory Analysis
2) Pitch Map
3) Pie Graph

# Methodology
A] Pre-processing the video:
The inﬁnite loop is used so that the web camera captures the frames in every instance and is open during the entire course of the program. After capturing the live stream frame by frame we are converting each frame in BGR colour space(the default one) to HSV colour space.
Now we know how to convert BGR image to HSV, we can use this to extract a coloured object.
B] Ball Tracking:
a) Constructing Mask:
Construct a mask for the colour ”green”, then perform a series of dilations and erosions to remove any small blobs left in the mask.
b) Contour Detection:
Find contours in the mask. Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid.
Thresholding is done initially for green colour levels using Gaussian blur and colour extraction technique.
C] Determining the Trajectory:
[1] Draw the circle and centroid on the frame, then update the list of tracked points.
[2] Update the points queue.
[3] Loop over the set of tracked points.
[4] Display the frame on screen.
D] Plotting the Pitch Map:
[1] Analyse the detected set of points so as to get the position of ball on the pitch.
[2] Plot the pitch and plot the sorted points on the frame containing the pitch.
