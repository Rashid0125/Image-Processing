import os
import cv2 
from PIL import Image 
import glob
import numpy as np
  
# Function to extract frames
def FrameCapture(path):
    try:
        # Path to video file
        vidObj = cv2.VideoCapture(path)
        # Used as counter variable
        count = 0
        # checks whether frames were extracted
        success = 1
        while success:
            # function extract frames
            success, image = vidObj.read()
            # Saves the frames with frame-count
            cv2.imwrite("frames/frame%d.jpg" % count, image)
            count += 1
    except Exception as e:
        print(e)
FrameCapture("task_2_video.mp4")

def hsv_masking(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([33,79,25])
    upper_hsv = np.array([72, 255, 255])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        center = (int((x+(x+w))/2),int((y+(y+h))/2))
        radius = int((((x-(x+w))**2 + (y-(y+h))**2)**0.5)/8)
        cv2.circle(img, center, radius, (0,0,255), -1)
    return img 

!mkdir gen_img
for img_name in os.listdir("frames"):
    img = cv2.imread("frames/"+img_name)
    hsv_gen = hsv_masking(img)
    cv2.imwrite(f"gen_img/{img_name}",hsv_gen)
    
def generate_video():
    image_folder = 'gen_img' 
    video_name = 'output.mp4'
      
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
     
    # Array images should only consider
    # the image files ignoring others if any
    print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
  
    video = cv2.VideoWriter(video_name, fourcc=0, fps=25,frameSize= (width, height)) 
    # Appending the images to the video one by one
    for i in range(len(images)): 
        img = cv2.imread(os.path.join(image_folder, f"frame{i}.jpg"))
        video.write(img) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
    

# Calling the generate_video function
generate_video()