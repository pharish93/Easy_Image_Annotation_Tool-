# Free Hand Drawing for image Annotation
# Author :- Harish Pullagurla ( hpullag@ncsu.edu )
# Last Updated :- 19th March 2017
# How to use :-
# 1. put images in the images folder
# 2. draw pattern on image
# 3. press Esc
# 4. Enter the image label value
# 5. Press 1 to continue annotating the same image
# Handling errors
# 6. Press 0 in the image lable value if you feel you did some mistake in selecting during free hand drawing as '0' is the base class
# 7. Try to draw closed loops during free hand drawing , else fulling dosent happen

import cv2
import numpy as np 
import os

drawing=False # true if mouse is pressed
mode=True # if True, draw rectangle. Press 'm' to toggle to curve
pt = []
file_locations = []

# mouse callback function
def freehand_draw(event,former_x,former_y,flags,param):
    global current_former_x,current_former_y,drawing, mode

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        current_former_x,current_former_y=former_x,former_y
        pt.append([former_x,former_y])

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if mode==True:
                cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(255,255,255),2)
                cv2.line(im2, (current_former_x, current_former_y), (former_x, former_y), 255, 2)
                current_former_x = former_x
                current_former_y = former_y
                pt.append([former_x, former_y])
                #print former_x,former_y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode==True:
            cv2.line(im,(current_former_x,current_former_y),(former_x,former_y),(255,255,255),2)
            cv2.line(im2,(current_former_x,current_former_y),(former_x,former_y),255,2)
            current_former_x = former_x
            current_former_y = former_y
            pt.append([former_x, former_y])
    return former_x,former_y    


# Main Program starts here

directory = os.getcwd()
directory_1 = directory + '\\Images\\'

for filename in os.listdir(directory_1):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        file_locations.append(os.path.join(directory_1, filename))
        continue
    else:
        continue

for h in range(len(file_locations)):
    filename = file_locations[h]
    im_base = cv2.imread(filename)
    #im = cv2.resize(im_base,(400,300),fx = 1,fy =1)
    im = im_base
    im_annotated = 100*np.ones((np.size(im,0),np.size(im,1)),dtype='uint8')
    response = '1'

    while(response == '1'):
        #print response
        im2 = np.zeros((np.size(im,0),np.size(im,1)),dtype='uint8')
        cv2.namedWindow("colour image")
        cv2.setMouseCallback('colour image',freehand_draw)

        while(1):
            cv2.imshow('colour image',im)
            k=cv2.waitKey(1)&0xFF
            if k==27:
                break

        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(im2, cv2.MORPH_CLOSE, kernel)
        # Copy the thresholded image.
        im_floodfill = closing.copy()

        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels than the image.
        h, w = im2.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255)
        # Invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        # Combine the two images to get the foreground.
        im_out = closing | im_floodfill_inv

        cv2.imshow("Foreground", im_out)
        cv2.waitKey(10)

        category = raw_input("enter the label number")
        if category == 500:
            print 'invalied_catogree'
            continue
			
        img_rows, img_cols = im_out.shape
        for i in range(img_rows):
            for j in range(img_cols):
                if im_out[i,j] == 255 :
                    im_annotated[i,j] = category
        #cv2.imshow("final label map", im_annotated)
        k=cv2.waitKey(1)&0xFF
        if k==97:
            break
        response = raw_input('press 1 to continue')
        cv2.destroyAllWindows()

    image_name = filename.split(directory_1)
    image_name_1 = image_name[1].split('.')
    filename_annotated_image = directory +'\\Annotated\\'+image_name_1[0]+'_annotated_image.png'
    finished_labeling =  directory +'\\Finished_Labeling\\'+ str(image_name[1])
    os.rename(filename,finished_labeling)
    cv2.imwrite(filename_annotated_image,im_annotated)
    cv2.destroyAllWindows()
