import cv2
import time
import glob
import os
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0                  #the loop starts with zero status
    check, frame = video.read()
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)


    if first_frame is None:
        first_frame = grey_frame_gau


    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)


    thresh_frame=cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]    # a need to define the pixels by treshold, the lower the whiter, the higher the darker
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) # tha last brackets are color of the rectangle, number 3 is width
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)
        clean_folder()     # the os removes the images after

    print(status_list)

    cv2.imshow("My Video", frame)
    key = cv2.waitKey(1)


    if key == ord("q"): #if you push the q button the camera will be turned off
        break

video.release()
