import cv2
import glob
import pandas as pd
import drone2.nmsiou as dn
csv_path = r'nopeoplemachine\csv\img1088'
no_nms = r'nopeoplemachine\no_nms\img1088'
original_crop_img = r'nopeoplemachine\crop\img1088'
detect_img = r'nopeoplemacjine\yolov7\runs\detect\third1088'
def inward():
    filelist = glob(csv_path+"\\.*csv")
    count =0
    for item in filelist:
        dellist = []
        file = pd.read_csv(item,header = 0,names = ["id","x","y","w","h","conf","IDcode"])
        Fname = item.split("\\")[-1]
        cn = Fname.split(".")[0]
        image = cv2.imread("nopeoplemachine\public"+ "\\"+ cn + ".png")
        (imgheight,imgwidth,rgb) = image.shape
        for i in range(len(file["id"])):
            if imgwidth == 1920:
                if (file["IDcode"][i] == "3_1") and ((int(file["x"][i]) ) < 960):
                    dellist.append(i)
                elif (file["IDcode"][i] == "2_1") and ((int(file["x"][i]) + int(file["w"][i]))> 1376) :
                    dellist.append(i)
                elif (file["IDcode"][i] == "2_1") and  (int(file["x"][i]) < 544) :
                    dellist.append(i)
                elif (file["IDcode"][i] == "1_1") and  ((int(file["x"][i]) + int(file["w"][i]))> 960) :
                    dellist.append(i)
            else:
                if (file["IDcode"][i] == "3_1") and (int(file["x"][i]) < 384):
                    dellist.append(i)
                elif (file["IDcode"][i] == "2_1") and ((int(file["x"][i])+ int(file["w"][i])) > 1088) :
                    dellist.append(i)
                elif (file["IDcode"][i] == "2_1") and  (int(file["x"][i]) < 256) :
                    dellist.append(i)
                elif (file["IDcode"][i] == "1_1") and  ((int(file["x"][i]) + int(file["w"][i])) > 960) :
                    dellist.append(i)
        count += len(file["id"])
        file.drop(file.index[dellist],axis = 0,inplace = True)
        file.to_csv(no_nms + "\\" + cn + ".csv" ,index = 0)        

def nms():
    dn.put_1500csv(modelpath = no_nms,mergepath = r"nopeoplemachine\nms\model1088")

def main():
    path_IMG = glob.glob(original_crop_img + "\\*.png")
    for item in path_IMG:
        img = item.split("\\")[-1]
        img = img.split(".")[0]
        num = img[:3]
        name = img[3:]
        id = []
        x1 = []
        y1 = []
        w1 = []
        h1 = []
        conf = []
        image = cv2.imread(item)
        (imgheight,imgwidth,rgb) = image.shape
        
        try:
            with open(detect_img + "\\" + img + ".txt" ) as f:
                for line in f.readlines():
                    s = line.split(' ')
                    id.append(int(s[0]))
                    x1.append(float(s[1]))
                    y1.append(float(s[2]))
                    w1.append(float(s[3]))
                    h1.append(float(s[4]))
                    conf.append(float(s[5][:-1]))
            f2=open(csv_path+ "\\" + name + ".csv",'a+')
            for a in range(len(id)):
                w = int(w1[a] * imgwidth)
                h = int(h1[a] * imgheight)
                x = int((x1[a]*imgwidth)-(w/2))
                y = int((y1[a]*imgheight)-(h/2))
                if num =='3_1':
                    if imgheight == 1080 and imgwidth == 1088:
                        x = x + 832
                    else:
                        x = x + 256
                if num == '2_1':
                    if imgheight == 1080 and imgwidth == 1088:
                        x = x + 416
                    else:
                        x = x + 128
                
                f2.write(str(id[a])+","+str(x)+","+str(y)+","+str(w)+","+str(h)+","+str(conf[a])+','+str(num)+'\n')
            f2.close()
        except:
            continue
    inward()
    nms()

if __name__ == "__main__":
    main()