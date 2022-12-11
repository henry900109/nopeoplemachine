import cv2
import os
import glob
from tqdm import tqdm,trange
from time import sleep

# crop image
# - file: image path
# - crop_path: path to save cropped images
def crop_image(file,crop_path,size):
    if size == 640:
        x1 = [0,370,910,1280]
        y1 = [0,440]

        x2 = [0,352,704]
        y2 = [0,80]

    elif size == 1088:
        x1 = [0,416,832]
        y1 = [0]

        x2 = [0,128,256]
        y2 = [0]

    # get image name
    img_name = file.split('\\')[-1]

    # read image
    img = cv2.imread(file)
    
    # get image width and height
    height, width, _ = img.shape

    # crop image
    if size == 640:
        if height == 1080 and width == 1920:
            for i in range(len(x1)):
                for j in range(len(y1)):
                    crop_img = img[y1[j]:y1[j]+size, x1[i]:x1[i]+size]
                    cv2.imwrite(crop_path +"\\img640\\"+ '{}_{}{}'.format(i+1,j+1,img_name), crop_img)
        elif height == 720 and width == 1344:
            for i in range(len(x2)):
                for j in range(len(y2)):
                    crop_img = img[y2[j]:y2[j]+size, x2[i]:x2[i]+size]
                    cv2.imwrite(crop_path +"\\img640\\"+ '{}_{}{}'.format(i+1,j+1,img_name), crop_img)
        else:
            return print('{} Image size not supported, image size = {},{}'.format(img_name,height,width))   
    else:
        if height == 1080 and width == 1920:
            for i in range(len(x1)):
                for j in range(len(y1)):
                    crop_img = img[y1[j]:y1[j]+size, x1[i]:x1[i]+size]
                    cv2.imwrite(crop_path +"\\img1088\\"+ '{}_{}{}'.format(i+1,j+1,img_name), crop_img)
        elif height == 720 and width == 1344:
            for i in range(len(x2)):
                for j in range(len(y2)):
                    crop_img = img[y2[j]:y2[j]+size, x2[i]:x2[i]+size]
                    cv2.imwrite(crop_path +"\\img1088\\"+ '{}_{}{}'.format(i+1,j+1,img_name), crop_img)
        else:
            return print('{} Image size not supported, image size = {},{}'.format(img_name,height,width))   


# read label data
# - file: original label path
# - sp: split character (default = ',')
def read_label(file,sp = ','):
    id = []
    x = []
    y = []
    w = []
    h = []
    conf = []
    
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            s = line.split(sp)
            id.append(int(s[0]))
            x.append(int(s[1]))
            y.append(int(s[2]))
            w.append(int(s[3]))
            h.append(int(s[4]))
            # conf.append(float(s[5]))
    
    return id,x,y,w,h

# get image size
# - file: original image path
def image_size(file,img_type='.png'):
    image_path = file.split('.')[0] + img_type
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    return height, width

# crop label
# - file: original label path
def crop_label(file,crop_label_path,size,img_type='.png'):
    # file name
    name = file.split('\\')[-1].split('.')[0]
    file_path = file.split(name)[0]
    file_path = file_path + name + ".txt"
    # crop path
    path = crop_label_path
    # read label data
    id,x,y,w,h = read_label(file_path)
    
    # get image size
    height, width = image_size(file,img_type)

    if size == 640:
        x1 = [370,910,1280]
        y1 = [440]

        x2 = [352,704]
        y2 = [80]

    elif size == 1088:
        x1 = [416,832]
        y1 = [0]

        x2 = [128,256]
        y2 = [0]
    if size == 640:
    # open file and write label data
        crop1 = open(path + '//img640//1_1' + name + '.txt', 'w+')
        crop2 = open(path + '//img640//2_1' + name + '.txt', 'w+')
        crop3 = open(path + '//img640//3_1' + name + '.txt', 'w+')
        crop4 = open(path + '//img640//4_1' + name + '.txt', 'w+')

        crop5 = open(path + '//img640//1_2' + name + '.txt', 'w+')
        crop6 = open(path + '//img640//2_2' + name + '.txt', 'w+')
        crop7 = open(path + '//img640//3_2' + name + '.txt', 'w+')
        crop8 = open(path + '//img640//4_2' + name + '.txt', 'w+')

        # crop label
        if height == 1080 and  width == 1920:
            for i in range(len(id)):
                if y[i] < 640:
                    if x[i] < 640:
                        print('oooooooooooooooooooooooooooooooooooo')
                        crop1.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 370 <= x[i] < 1010:
                        crop2.write(str(id[i]) + ' ' + str(x[i]-x1[0]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i]) + '\n')
                    if 910 <= x[i] < 1550:
                        crop3.write(str(id[i]) + ' ' + str(x[i]-x1[1]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i]) + '\n')
                    if size == 640:
                        if 1280 <= x[i] < 1920:
                            crop4.write(str(id[i]) + ' ' + str(x[i]-x1[2]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                        
                if y[i] >= 440:
                    if x[i] < 640:
                        crop5.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]-y1[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 370 <= x[i] < 1010:
                        crop6.write(str(id[i]) + ' ' + str(x[i]-x1[0]) + ' ' + str(y[i]-y1[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 910 <= x[i] < 1550:
                        crop7.write(str(id[i]) + ' ' + str(x[i]-x1[1]) + ' ' + str(y[i]-y1[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if size == 640:
                        if 1280 <= x[i] < 1920:
                            crop8.write(str(id[i]) + ' ' + str(x[i]-x1[2]) + ' ' + str(y[i]-y1[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')

        elif height == 720 and width == 1344:
            for i in range(len(id)):
                if y[i] < 640:
                    if x[i] < 640:
                        crop1.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 352 <= x[i] < 992:
                        crop2.write(str(id[i]) + ' ' + str(x[i]-x2[0]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 704 <= x[i] < 1344:
                        crop3.write(str(id[i]) + ' ' + str(x[i]-x2[1]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    
                    
                if y[i] >= 80:
                    if x[i] < 640:
                        crop5.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]-y2[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 352 <= x[i] < 992:
                        crop6.write(str(id[i]) + ' ' + str(x[i]-x2[0]) + ' ' + str(y[i]-y2[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    if 704 <= x[i] < 1344:
                        crop7.write(str(id[i]) + ' ' + str(x[i]-x2[1]) + ' ' + str(y[i]-y2[0]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
        
        crop8.close()
        crop7.close()
        crop6.close()
        crop5.close()
        crop4.close()
        crop3.close()
        crop2.close()
        crop1.close()
    else:
        # open file and write label data
        crop9 = open(path +'//img1088//1_1' + name + '.txt', 'w+')
        crop10 = open(path +'//img1088//2_1' + name + '.txt', 'w+')
        crop11 = open(path +'//img1088//3_1' + name + '.txt', 'w+')

        # crop label
        if height == 1080:
            for i in range(len(id)):
                if x[i] < 1088:
                    crop9.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                if 416 <= x[i] < 1504:
                    crop10.write(str(id[i]) + ' ' + str(x[i]-x1[0]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i]) + '\n')
                if 832 <= x[i]:
                    crop11.write(str(id[i]) + ' ' + str(x[i]-x1[1]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i]) + '\n')
                
        elif height == 720:
            for i in range(len(id)):
                if x[i] < 1088:
                    crop9.write(str(id[i]) + ' ' + str(x[i]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                if 128 <= x[i] < 1216:
                    crop10.write(str(id[i]) + ' ' + str(x[i]-x2[0]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                if 256 <= x[i]:
                    crop11.write(str(id[i]) + ' ' + str(x[i]-x2[1]) + ' ' + str(y[i]) + ' ' + str(w[i]) + ' ' + str(h[i])  + '\n')
                    
        crop11.close()
        crop10.close()
        crop9.close()
    
    return

# remove empty label file with corresponding image
# - crop_label: cropped label
# - crop_image: cropped image
def remove_empty(crop_label,crop_image,img_type = '.png'):
    if os.stat(crop_label).st_size == 0:
        os.remove(crop_label)
        os.remove(crop_label.split('.')[0] + img_type)
    return

# Delete box outside of image
# - cropped_label: cropped label
def delete_outside_box(cropped_label):
    with open(cropped_label, 'r') as f:
        lines = f.readlines()
        f.close()
    with open(cropped_label, 'w') as f:
        for line in lines:
            id, x, y, w, h = line.split(' ')
            if int(x) + int(w) > 640 or int(y) + int(h) > 640:
                continue
            else:
                f.write(line)
        f.close()
    return

# Normalize label
# - cropped_label: cropped label
def normalize_label(cropped_label,img_type = '.png'): 
    with open(cropped_label, 'r') as f:
        lines = f.readlines()
        f.close()
    with open(cropped_label, 'w') as f:
        for line in lines:
            id, x, y, w, h = line.split()
            x = float(x) + float(w)/2
            y = float(y) + float(h)/2
            w = float(w)
            h = float(h)
            image = cropped_label.split('.')[0] + img_type
            height, width = image_size(image)
            x = x/width
            y = y/height
            w = w/width
            h = h/height
            f.write(str(id) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')
        f.close()
    return 


# main
# - original_img_path: path to images
# - crop_img_path: path to save cropped images
# - crop_label_path: path to save cropped labels
def main(img_type = '.png'):
    # crop image
    files = glob.glob(original_img_path + '\\*' + img_type)
    for file in tqdm(files,desc='Cropping image'):
        crop_image(file,crop_img_path,size=640)
        crop_image(file,crop_img_path,size=1088)
        sleep(0.001)
    

    # crop label
    for file in tqdm(files,desc='Cropping label'):
        crop_label(file,crop_label_path,size=640,img_type='.png')
        crop_label(file,crop_label_path,size=1088,img_type='.png')
        sleep(0.001)

    # remove empty label file with corresponding image
    cropped_label640 = glob.glob(crop_label_path + '\\img640\\*' + '.txt') 
    cropped_image640 = glob.glob(crop_img_path + '\\img640\\*' + img_type)
    # Delete box outside of image
    for i in trange(len(cropped_label640),desc='Deleting box outside of image'):
        delete_outside_box(cropped_label640[i])
    # Normalize label
    for i in trange(len(cropped_label640),desc='Normalizing label'):
        normalize_label(cropped_label640[i],img_type = '.png')
    try:
        for i in trange(len(cropped_label640),desc='Removing empty label'):
            remove_empty(cropped_label640[i],cropped_image640[i])
    except FileNotFoundError:
        print('File not found: ' + cropped_label640[i] + ' or ' + cropped_image640[i])


    cropped_label1088 = glob.glob(crop_label_path + '\\img1088\\*' + '.txt') 
    cropped_image1088 = glob.glob(crop_img_path + '\\img1088\\*' + img_type)
    # Delete box outside of image
    for i in trange(len(cropped_label1088),desc='Deleting box outside of image'):
        delete_outside_box(cropped_label1088[i])
    # Normalize label
    for i in trange(len(cropped_label1088),desc='Normalizing label'):
        normalize_label(cropped_label1088[i],img_type = '.png')
    try:
        for i in trange(len(cropped_label1088),desc='Removing empty label'):
            remove_empty(cropped_label1088[i],cropped_image1088[i])
    except FileNotFoundError:
        print('File not found: ' + cropped_label1088[i] + ' or ' + cropped_image1088[i])


original_img_path = r'nopeoplemachine\train_offical'
crop_img_path = r'nopeoplemachine\crop'
crop_label_path = r'nopeoplemachine\crop'

if __name__ == "__main__":
    main()