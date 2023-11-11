import cv2
import numpy as np
from rembg import remove
from PIL import Image
import os
import shutil


if os.path.exists("cropped_folder"):
    shutil.rmtree("cropped_folder")
    os.makedirs("cropped_folder")
else:
    os.makedirs("cropped_folder")
    
if os.path.exists("rembg"):
    shutil.rmtree("rembg")
    os.makedirs("rembg")
    
else:
    os.makedirs("rembg")

while True:
    # Read image
    input_image = input("Please select the input image 1 , 2 , q (for exit)     :    ")
    if input_image=="1" or input_image=="2":
        image = cv2.imread("TEST_IMAGES/"+input_image+".jpg")
        # Select ROI
        r = cv2.selectROI("select the area", image)
        cv2.imshow("Cropped image", image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
        # # Crop image
        cropped_image = image[int(r[1]):int(r[1]+r[3]), 
                              int(r[0]):int(r[0]+r[2])]
        if len(list(cropped_image))>1:
            #save cropped image
            cv2.imwrite("cropped_folder/cropped_img.jpg",cropped_image)

            #rembg processing
            input_path = 'cropped_folder/cropped_img.jpg' # input image path
            output_path = 'rembg/image.png' # output image path

            input1 = Image.open(input_path) # load image
            output = remove(input1) # remove background
            output.save(output_path) # save image

            img = cv2.imread(output_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(gray,0, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cont = contours[:]
            for i in cont:
                for j in range(len(i)):
                    i[j][0][0] = i[j][0][0]+int(r[0])
                    i[j][0][1] = i[j][0][1]+int(r[1])

            img_gen = cv2.drawContours(image, cont, -1, (0, 255, 0), 3)
            cv2.imshow("Output Image", img_gen)
            cv2.waitKey(0)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            elif cv2.waitKey(0) & 0xFF == ord('c'):
                cv2.destroyAllWindows()
                pass
            
        else:
            img_invalid = cv2.imread("invalid_input_image/invalid.png")
            cv2.imshow("invalid input", img_invalid)
            cv2.waitKey(0)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
    elif input_image=="q":
        print("Exit Successful, Thank you!!")
        break
    else:
        print("Please input the correct image number")