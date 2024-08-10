# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 12:56:33 2024

@author: amitc
"""

import os
import fileinput
from pathlib import Path
import cv2
import numpy as np
import math
from PIL import Image, ExifTags


def Image_orientation_fix(Image_full_path):
    # Open the image using PIL
    img_pil = Image.open(Image_full_path)
    
    # Retrieve EXIF data
    exif = img_pil._getexif()
    
    
    # Find the orientation key (if it exists)
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    
    # Apply orientation correction if needed
    if exif and orientation in exif:
        orientation_value = exif[orientation]
        #print(orientation_value)
        
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
        if orientation_value == 3:
            #img_pil = img_pil.rotate(180, expand=True)
            cv2.rotate(img, cv2.ROTATE_180)
            
        elif orientation_value == 6:
            #img_pil = img_pil.rotate(270, expand=True)
            cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif orientation_value == 8:
            #img_pil = img_pil.rotate(90, expand=True)
            cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def plot_annotation(text_file_path,img):
    with open(text_file_path, 'r') as file:
        file.readline()
        
        for line in file:
            #print(line)
            x = int(line.split(',')[5])
            y = int(line.split(',')[6])
            #print(f"x:{x}, y:{y}")
            
            e_1 = int(line.split(',')[7])
            e_2 = int(line.split(',')[8])
            
            radius_of_circle = int(math.sqrt(math.pow((e_1-x),2) + math.pow((e_2-y),2)))
            
            width_height_of_box = 2 * radius_of_circle
            
            xmin = int(x - width_height_of_box)
            xmax = int(x + width_height_of_box)
            ymin = int(y - width_height_of_box)
            ymax = int(y + width_height_of_box)
            
            Top_left_corner = (xmin, ymin)
            Bottom_right_corner = (xmax, ymax)

            
            #cv2.rectangle(img, Top_left_corner, Bottom_right_corner, (0, 255, 0), 2) # If required bounding box
            
            cv2.circle(img, (x, y), radius_of_circle, (0, 0, 255), 5) # If required cirlce bounding
            
            #cv2.circle(img, (x, y), 4, (0, 255, 0), 3) # If required dot
            
    return img

Dir_path='C:/Users/amitc/Downloads/Malaria-Priyanka Roy/NIH-NLM-ThickBloodSmearsPV/NIH-NLM-ThickBloodSmearsPV/'
Dir_name='All_annotations/'


full_path= os.path.join(Dir_path , Dir_name)

Image_path = os.path.join(Dir_path, 'All_PvTk/',)

dir_list=os.listdir(full_path)


for i in range(len(dir_list)):
    print(dir_list[i])
    count = 0

    text_file_list=os.listdir(full_path + dir_list[i])
    
    for z in range(len(text_file_list)):

        text_file_path= os.path.join(full_path + dir_list[i] +'/'+ text_file_list[z])
        Image_full_path= os.path.join(Image_path + dir_list[i] +'/'+ text_file_list[z].replace('.txt', '.jpg'))
        
        if os.path.exists(text_file_path) and os.path.exists(Image_full_path):

            #print(os.path.basename(text_file_path),os.path.basename(Image_full_path))
            Dir_1_path =os.path.join(Dir_path+'Modified_dataset/' + 'Original_dataset-Rotated/'+ dir_list[i])
            Dir_2_path = os.path.join(Dir_path+'Modified_dataset/' + 'Parasitized-Annotation/'+ dir_list[i])
           
            if not os.path.exists(Dir_1_path):
                try:
                    os.makedirs(Dir_1_path)
                except OSError as e:
                    print(f"Error creating folder")
                

            if not os.path.exists(Dir_2_path):
                try:
                    os.makedirs(Dir_2_path)
                except OSError as e:
                    print(f"Error creating folder")
                
            
            # Save images after the rotation

            save_rotate_image_path=os.path.join(Dir_1_path + '/' + text_file_list[z].replace('.txt', '.jpg'))
            
            rotated_image = Image_orientation_fix(Image_full_path)
            
            cv2.imwrite(save_rotate_image_path,rotated_image)
            
            count +=1 


            # Save annotated image
            save_annotated_image=os.path.join(Dir_2_path + '/' + text_file_list[z].replace('.txt', '.jpg'))
            
            cv2.imwrite(save_annotated_image,plot_annotation(text_file_path,rotated_image))
                  
                    
        else:
            print(os.path.basename(text_file_path),os.path.basename(Image_full_path))
            continue
    print(count)

        


    
