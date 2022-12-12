import os
import glob
import cv2
import pandas as pd
import glob
from tqdm import tqdm
from time import sleep
import drone2.nmsiou as dn


# renormalize label data
# - file: output label path after detection
# - csv_path: path to save csv file
def renorm(output_label,csv_path,sp = ','):
    name = output_label.split("\\")[-1].split(".")[0]
    id = []
    x1 = []
    y1 = []
    w1 = []
    h1 = []
    conf = []

    with open(output_label) as f:
        for line in f.readlines():
            s = line.split(' ')
            id.append(int(s[0]))
            x1.append(float(s[1]))
            y1.append(float(s[2]))
            w1.append(float(s[3]))
            h1.append(float(s[4]))
            conf.append(float(s[5]))
    
    f2=open(csv_path +'\\'+ name + ".csv",'w+')
    for a in range(len(id)):
        w = int(w1[a] * 640)
        h = int(h1[a] * 640)
        x = int((x1[a] * 640)-(w/2))
        y = int((y1[a] * 640)-(h/2))

        f2.write(str(id[a])+","+str(x)+","+str(y)+","+str(w)+","+str(h)+","+str(conf[a])+'\n')
    f2.close()

# read label data
# - file: output label path after detection
def read_label(file,sp = ','):
    id = []
    x = []
    y = []
    w = []
    h = []
    conf = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            s = line.split(sp)
            id.append(int(s[0]))
            x.append(int(s[1]))
            y.append(int(s[2]))
            w.append(int(s[3]))
            h.append(int(s[4]))
            conf.append(float(s[5]))
    return id,x,y,w,h,conf

# get image size
# - file: original image path
def image_size(file,img_type='.png'):
    image_path = file.split('.')[0] + img_type
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    return height, width
           

# crop label
# - csv_file: label path after renormalization
# - original_img_path: original image path
def re_label(csv_file,original_img_path,img_type='.png'):
    # file name
    name = csv_file.split('\\')[-1].split('.')[0]
    label = name[:3]
    # print(name[3:])
    # file path
    path = csv_file.split(name)[0]

    # read label data
    id,x,y,w,h,conf = read_label(csv_file)
    # get image size
    height, width = image_size(original_img_path +'//'+ name[3:] + img_type)

    # open file and write
    crop1 = open(path +  name + '.csv', 'w+')
    crop2 = open(path +  name + '.csv', 'w+')
    crop3 = open(path +  name + '.csv', 'w+')
    crop4 = open(path +  name + '.csv', 'w+')

    crop5 = open(path + name + '.csv', 'w+')
    crop6 = open(path + name + '.csv', 'w+')
    crop7 = open(path + name + '.csv', 'w+')
    crop8 = open(path + name + '.csv', 'w+')

    # crop label and delete label which is out of range
    if height == 1080 and width == 1920:
        for i in range(len(id)):
            if label in ['1_1','2_1','3_1','4_1']:
                if y[i] < 560:
                    if label == '1_1':
                        if x[i] < 560 or x[i] + w[i]< 560:
                            crop1.write(str(id[i]) + ',' + str(x[i]) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '2_1':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop2.write(str(id[i]) + ',' + str(x[i]+370) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '3_1':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop3.write(str(id[i]) + ',' + str(x[i]+910) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '4_1':
                        if (80 <= x[i]) or (80 <= (x[i] + w[i])):
                            crop4.write(str(id[i]) + ',' + str(x[i]+1280) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
            elif label in ['1_2','2_2','3_2','4_2']:        
                if y[i] >= 80:
                    if label == '1_2':
                        if (x[i] < 560) or ((x[i] + w[i])< 560):
                            crop5.write(str(id[i]) + ',' + str(x[i]) + ',' + str(y[i]+440) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '2_2':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop6.write(str(id[i]) + ',' + str(x[i]+370) + ',' + str(y[i]+440) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '3_2':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop7.write(str(id[i]) + ',' + str(x[i]+910) + ',' + str(y[i]+440) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '4_2':
                        if (80 <= x[i]) or (80 <= (x[i] + w[i])):
                            crop8.write(str(id[i]) + ',' + str(x[i]+1280) + ',' + str(y[i]+440) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')

    elif height == 720 and width == 1344:
        for i in range(len(id)):
            if label in ['1_1','2_1','3_1','4_1']:
                if y[i] < 590:
                    if label == '1_1':
                        if (x[i] < 560) or ((x[i] + w[i])< 560):
                            crop1.write(str(id[i]) + ',' + str(x[i]) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '2_1':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop2.write(str(id[i]) + ',' + str(x[i]+352) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '3_1':
                        if (80 <= x[i]) or (80 <= (x[i] + w[i])):
                            crop3.write(str(id[i]) + ',' + str(x[i]+704) + ',' + str(y[i]) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    
            elif label in ['1_2','2_2','3_2','4_2']: 
                if y[i] >= 50:
                    if label == '1_2':
                        if (x[i] < 560) or ((x[i] + w[i])< 560):
                            crop5.write(str(id[i]) + ',' + str(x[i]) + ',' + str(y[i]+80) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '2_2':
                        if (80 <= x[i] < 560) or (80 <= (x[i] + w[i]) < 560):
                            crop6.write(str(id[i]) + ',' + str(x[i]+352) + ',' + str(y[i]+80) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
                    elif label == '3_2':
                        if (80 <= x[i]) or (80 <= (x[i] + w[i])):
                            crop7.write(str(id[i]) + ',' + str(x[i]+704) + ',' + str(y[i]+80) + ',' + str(w[i]) + ',' + str(h[i]) + ',' + str(conf[i]) + '\n')
    
    crop8.close()
    crop7.close()
    crop6.close()
    crop5.close()
    crop4.close()
    crop3.close()
    crop2.close()
    crop1.close()
    return

# combine labels
# - csv_label: path to csv label
# - final: path to final output
def combine_labels(csv_label,no_nms):
    img_name = csv_label.split("\\")[-1].split(".")[0]
    # img_name = img_name.split(".")[0]
    name = img_name[3:]
    label = img_name[:3]
    # write new file with same name
    f2=open(no_nms +'\\'+ name + ".csv",'a+')
    with open(csv_label) as f:
        for line in f.readlines():
            new = line.strip('\n')
            f2.write(new + ',' + label + '\n')
    f2.close()
    return

def nms():
    dn.put_1500csv(model640path = no_nms,mergepath = r"nopeoplemachine\nms\model640")
# main
# - output_label_path: path to output label
# - origin_img_path: path to origin image
# - csv_path: path to csv file after renormalize
# - final: path to final output
def main():
    label_path = glob.glob(output_label_path + '\\*.txt')

    # renormalize labels
    for file in tqdm(label_path,desc='Renormalize detection labels'):
        renorm(file,csv_path)
        sleep(0.001)

    csv_label = glob.glob(csv_path + '\\*.csv')
    # Transform labels to original
    for file in tqdm(csv_label,desc='Transform detection labels'):
        re_label(file,origin_img_path)
        sleep(0.001)

    # combine labels
    for file in tqdm(csv_label,desc='Combine detection labels'):
        combine_labels(file,no_nms)
        sleep(0.001)
    nms()

output_label_path = r'nopeoplemachine\output_label_path'
origin_img_path = r'nopeoplemachine\train_offical'
csv_path = r'nopeoplemachine\csv'
no_nms = r'nopeoplemachine\no_nms\img640'
if __name__ == "__main__":
    main()




    
