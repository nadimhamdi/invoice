# -*- coding: utf-8 -*-
import os
import cv2
import imutils
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from operator import itemgetter
import itertools


########   fonction utile ###############
def imshow_components(labels):
    ### creating a hsv image, with a unique hue value for each label
    label_hue = np.uint8(179*labels/np.max(labels))
    ### making saturation and volume to be 255
    empty_channel = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, empty_channel, empty_channel])
    ### converting the hsv image to BGR image
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue==0] = 0
    ### returning the color image for visualising Connected Componenets
    return labeled_img
def detect_box(image,line_min_width=20):#use 80 for large pic
    gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    th1,img_bin = cv2.threshold(gray_scale,240,250,cv2.THRESH_BINARY)#230,250
    kernal6h = np.ones((1,line_min_width), np.uint8)
    kernal6v = np.ones((line_min_width,1), np.uint8)
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal6h)
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal6v)
    img_bin_final = img_bin_h | img_bin_v

    final_kernel = np.ones((3,3), np.uint8)
    img_bin_final=cv2.dilate(img_bin_final,final_kernel,iterations=1)
    ret, labels, stats,centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    #print(ret)
    if ret>40:
        stats,labels,centroids=detect_box(image,line_min_width+5)
    return stats,labels,centroids
def merge_common(lists):
    neigh = defaultdict(set)
    visited = set()
    for each in lists:
        for item in each:
            neigh[item].update(each)

    def comp(node, neigh=neigh, visited=visited, vis=visited.add):
        nodes = set([node])
        next_node = nodes.pop
        while nodes:
            node = next_node()
            vis(node)
            nodes |= neigh[node] - visited
            yield node

    for node in neigh:
        if node not in visited:
            yield sorted(comp(node))
def plot(image,cmap=None):
    plt.figure(figsize=(15,15))
    plt.imshow(image,cmap=cmap)
#########################################


########### Variable ####################
plot_flag=True
save_output=True
out_folder='outs'
#########################################




def TabulExecution(ImageName_sans_terminisant,NomTableau):
    in_file = os.path.join("Extraction/", "{}/{}".format(ImageName_sans_terminisant,NomTableau+'.png'))
    try:
        os.makedirs('Extraction/{}/Outs/{}/Image/'.format(ImageName_sans_terminisant, NomTableau))
    except:
        print('Extraction/{}/Outs/{}/Image'.format(ImageName_sans_terminisant, NomTableau)," existe deja")
    img = cv2.imread(os.path.join(in_file))
    image=img
    width,height,_=img.shape
    stats, labels,centroids = detect_box(image)
    cc_out = imshow_components(labels)
    coordonate_data = []
    id=0
    for (x, y, w, h, area),c in zip(stats,centroids):
        if (x==0 and y==0 and h==width and w==height) or w*h<1000 or w*h>width*height*0.5:# 1000 minimom aria of acase allowed
            pass#filtre les case non desire #dans ce cas si le tableau entier
        else:
            id=id+1
            surface=w*h
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            #image =cv2.circle(image, (int(c[0]),int(c[1])), 2, (0,0, 255), 2)
            #image = cv2.putText(image, str(id), (int(c[0]),int(c[1])),  cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 1, cv2.LINE_AA)
            ss=image[y:y+h, x:x+w]
            cv2.imwrite('Extraction/{}/Outs/{}/Image/{}_{}_{}_{}_{}.jpg'.format(ImageName_sans_terminisant,NomTableau,x, y, w, h, surface), ss)
            #print(surface)
            coordonate_data.append([surface,[c[0],c[1]],x, y, w, h,area,id])
    coordonate_data.sort(key=lambda x: x[0])
    coordonate_data=coordonate_data[::-1]
    #print (coordonate_data)
    if plot_flag:
        plot(cc_out)
        plot(image)

    if save_output:
        cv2.imwrite('Extraction/{}/Outs/{}/cc_out.jpg'.format(ImageName_sans_terminisant,NomTableau), cc_out)
        cv2.imwrite('Extraction/{}/Outs/{}/image.jpg'.format(ImageName_sans_terminisant,NomTableau), image)



    limite_centroide=25
    limite_point_depatr=5
    limite_point_depatry=100
    casex=[]
    casey=[]
    #print('coordonnet data {}'.format(coordonate_data))
    for pair in itertools.combinations(coordonate_data, 2):
        #print(*pair)
        if (abs(pair[0][2]-pair[1][2])<limite_point_depatr):
            casex.append([pair[0][7],pair[1][7]])
        else :
            casex.append([pair[0][7], pair[0][7]])
            casex.append([pair[1][7], pair[1][7]])


        #print('paire y {}'.format(abs(pair[0][3] - pair[1][3])))
        if (abs(pair[0][3]-pair[1][3])<limite_point_depatr):
            casey.append([pair[0][7],pair[1][7]])
        else :
            casey.append([pair[0][7], pair[0][7]])
            casey.append([pair[1][7], pair[1][7]])
    #print('casex : {}'.format(casex))
    #print('casey : {}'.format(casey))
    if len(coordonate_data)==1:
        casex.append([1,1])
        casey.append([1,1])
    '''
    #print(casey)
    #from functools import reduce
    #listeColonne=reduce(lambda x, y: ([i for i, j in zip(x,y) if i == j]), casex)
    #print(listeColonne)
    print(casex)
    tempvarlis=[]
    listcottin=[]
    for l in casex:
        tempvarliss=list(set(l) & set(tempvarlis))
        if tempvarliss==[]:
            listcottin.append(tempvarlis)
            tempvarlis = l
        tempvarlis = list(set(tempvarlis + l))
        print(tempvarliss)
        print (tempvarlis)
    listcottin.append(tempvarlis)
    listcottin.pop(0)
    print(listcottin)
    '''
    #print('casey {}'.format(casey))
    listcasex = list(merge_common(casex))
    listcasey = list(merge_common(casey))
    #print('listecasey {}'.format(listcasey))
    #print(listcasex)
    #print(listcasey)
    #print (coordonate_data)
    coordonatex=[]
    coordonatey=[]
    for i in listcasex:
        x=list(filter(lambda x:x[7]==i[0],coordonate_data))
        coordonatex.append(x[0][2])

    for i in listcasey:
        y=list(filter(lambda y:y[7]==i[0],coordonate_data))
        coordonatey.append(y[0][3])

    #print('coordonnerty {}'.format(coordonatey))
    xsorted=[x for _, x in sorted(zip(coordonatex,listcasex ))]
    ysorted=[y for _, y in sorted(zip(coordonatey,listcasey ))]

    DictIndexOfCSV={}
    for i in coordonate_data:

        DictIndexOfCSV[str(i[7])]={'data':i}
    for X_case in xsorted:
        #print(listcasex.index(X_case)+1)
        #print(X_case)
        for ind in X_case:
            di={"X":xsorted.index(X_case)}
            DictIndexOfCSV[str(ind)].update(di)
    for Y_case in ysorted:
        #print(listcasex.index(X_case)+1)
        #print(X_case)
        for ind in Y_case:
            di={"Y":ysorted.index(Y_case)}
            DictIndexOfCSV[str(ind)].update(di)
    #print(DictIndexOfCSV)
    import easyocr
    import pytesseract
    import xlwt
    from xlwt import Workbook
    from pytesseract import Output

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    custom_config = r'-l fra --psm 12'


    reader = easyocr.Reader(['fr'], gpu=False)
    #result = reader.readtext(in_file, detail=0)
    #result = pytesseract.image_to_string(in_file, config=custom_config)
    #print(result)
    extra_txt = img.copy()

    for key, value in DictIndexOfCSV.items():
        try:
            print(value['X'],value['Y'])

            #print(value['data'])
            x=value['data'][2]
            y=value['data'][3]
            w=value['data'][4]
            h=value['data'][5]
            id=value['data'][7]
            imm=image[y:y+h, x:x+w]
            extra_txt[y:y+h, x:x+w] = 255
            #im=cv2.cvtColor(imm, cv2.COLOR_BGR2GRAY)
            im=(((cv2.cvtColor(imm, cv2.COLOR_BGR2GRAY))))
            cv2.imwrite('Extraction/{}/Outs/{}/Image/{}.jpg'.format(ImageName_sans_terminisant, NomTableau,id), im)
            result = reader.readtext(im, detail=0)
            results=""
            for res in result:
                results=results+" "+res
            #result=pytesseract.image_to_string(im, config=custom_config)
            #datacsv[int(value['X'])][int((aa))]=result
            sheet1.write(int(value['Y']),int(value['X']), results)

            #print(id)
            #print (result)
        except:
            pass
    wb.save('Extraction/{}/Outs/{}/{}.xls'.format(ImageName_sans_terminisant, NomTableau,NomTableau))
    cv2.imwrite('Extraction/{}/Outs/{}/extratxt.jpg'.format(ImageName_sans_terminisant, NomTableau ), extra_txt)
    extratxt = pytesseract.image_to_string(extra_txt, config=custom_config)
    #print((extratxt))
    with open('Extraction/{}/Outs/{}/extra_txt.txt'.format(ImageName_sans_terminisant, NomTableau ), mode='w') as f:
        f.write(extratxt)
    """
    #convert to CSV
    import pandas as pd
    
    read_file = pd.read_excel('stackoverflow.xls',sheet_name='Sheet 1')
    read_file.to_csv('name.csv', index=None, header=True)
    """
    """
    pre_processed = pre_process_image(img, pre_file)
    text_boxes = find_text_boxes(pre_processed)
    cells = find_table_in_boxes(text_boxes)
    hor_lines, ver_lines = build_lines(cells)
    """
    '''
    # Visualize the result
    vis = img.copy()

    # for box in text_boxes:
    #     (x, y, w, h) = box
    #     cv2.rectangle(vis, (x, y), (x + w - 2, y + h - 2), (0, 255, 0), 1)

    for line in hor_lines:
        [x1, y1, x2, y2] = line
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

    for line in ver_lines:
        [x1, y1, x2, y2] = line
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imwrite(out_file, vis)
    '''
if __name__ == "__main__":
    TabulExecution("img66","TableRegion_17")
