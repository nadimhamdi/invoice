# -*- coding: utf-8 -*-
from pytesseract import image_to_string 
import os
import cv2

def para(ImageName_sans_terminisant,NomTableau):
    in_file = os.path.join("Extraction/", "{}/{}".format(ImageName_sans_terminisant,NomTableau+'.png'))
    try:
        os.makedirs('Extraction/{}/Outs/{}/Image/'.format(ImageName_sans_terminisant, NomTableau))
    except:
        print('Extraction/{}/Outs/{}/Image'.format(ImageName_sans_terminisant, NomTableau)," existe deja")
    img = cv2.imread(os.path.join(in_file))
    image=img

    cv2.imwrite('Extraction/{}/Outs/{}/Image/image.jpg'.format(ImageName_sans_terminisant,NomTableau), image)

    save_path='Extraction/{}/Outs/{}/Image/resultat.txt'.format(ImageName_sans_terminisant,NomTableau)
    text =  image_to_string(image)

    with open(save_path, mode = 'w') as f:
       f.write(text)
