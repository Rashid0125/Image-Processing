import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import os

!mkdir frames
!mkdir gen_imgs
#Extracting each frames from input video
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
FrameCapture("task_4_video.mp4")



# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose

# Setup the Pose function for images - independently for the images standalone processing.
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# Setup the Pose function for videos - for video processing.
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)

# Initialize mediapipe drawing class - to draw the landmarks points.
mp_drawing = mp.solutions.drawing_utils

def detectPose(image_pose, pose, draw=False, display=False):
    
    original_image = image_pose.copy()
    
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    
    resultant = pose.process(image_in_RGB)

    if resultant.pose_landmarks and draw:    

        mp_drawing.draw_landmarks(image=original_image, landmark_list=resultant.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                               thickness=3, circle_radius=3),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                               thickness=2, circle_radius=2))
        
        return original_image
    else:
        return image_pose
cnt=0
for pose_frame in os.listdir("frames/"):
    try:
        image_path = 'frames/'+pose_frame
        output = cv2.imread(image_path)
        pose_detected_img = detectPose(output, pose_image, draw=True, display=False)
        cv2.imwrite(f"gen_imgs/{pose_frame}",pose_detected_img)
    except Exception as e:
        print(e,cnt)
    cnt+=1
    
def generate_video():
    image_folder = 'gen_imgs' 
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
  
    video = cv2.VideoWriter(video_name, fourcc=0, fps=17,frameSize= (width, height)) 
    # Appending the images to the video one by one
    for i in range(len(images)): 
        img = cv2.imread(os.path.join(image_folder, f"frame{i}.jpg"))
        video.write(img) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
    

# Calling the generate_video function
generate_video()