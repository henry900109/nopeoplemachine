import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import glob

def normalize1088(img_type='.png'):
    IMG = glob.glob(train_offical+'\\*'+img_type)
    # print(IMG)
    for item in IMG:
        x = []
        y = []
        w = []
        h = []
        id = []
        #print(item)
        TXT = item.split(".")[0]
        img = TXT.split('\\')[-1]
        # print(TXT)
        image = cv2.imread(item)
        (imgheight,imgwidth,rgb) = image.shape
        with open(TXT+".txt") as f:
            for line in f.readlines():
                s = line.split(',')
                id.append(int(s[0]))
                x.append(int(s[1]))
                y.append(int(s[2]))
                w.append(int(s[3]))
                h.append(int(s[4]))
        
        f2=open(train_normalize+'\\'+img+".txt",'w+')
        for a in range(len(id)):
            x_min = x[a]
            x_max = (x[a]+w[a])
            y_min = y[a]
            y_max = (y[a]+h[a])
            x_center = (x_min+x_max)/2
            y_center = (y_min+y_max)/2
            f2.write(str(id[a])+" "+str(x_center/imgwidth)+" "+str(y_center/imgheight)+" "+str(w[a]/imgwidth)+" "+str(h[a]/imgheight)+'\n')
        f2.close

train_offical = r"nopeoplemachine\train_offical"
train_normalize = r"nopeoplemachine\train_normalize"
if __name__ == "__main__":
    normalize1088()