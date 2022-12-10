import pandas as pd
from glob import glob
import math
import torch

mergepath = r"nopeoplemachine\nms\merge"
model1088path = r"nopeoplemachine\nms\model1088"
model640path = r"nopeoplemachine\nms\model640"
resultpath = r"nopeoplemachine\nms\result.csv"

def bbox_iou(box1, box2, x1y1x2y2=True, GIoU=False, DIoU=False, CIoU=False, eps=1e-7):
    # Returns the IoU of box1 to box2. box1 is 4, box2 is nx4
    box2 = box2.T
    
    # Get the coordinates of bounding boxes
    if x1y1x2y2:  # x1, y1, x2, y2 = box1
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]
    else:  # transform from xywh to xyxy
        b1_x1, b1_x2 = box1[0] - box1[2] / 2, box1[0] + box1[2] / 2
        b1_y1, b1_y2 = box1[1] - box1[3] / 2, box1[1] + box1[3] / 2
        b2_x1, b2_x2 = box2[0] - box2[2] / 2, box2[0] + box2[2] / 2
        b2_y1, b2_y2 = box2[1] - box2[3] / 2, box2[1] + box2[3] / 2

    # Intersection area
    inter = (torch.min(b1_x2, b2_x2) - torch.max(b1_x1, b2_x1)).clamp(0) * \
            (torch.min(b1_y2, b2_y2) - torch.max(b1_y1, b2_y1)).clamp(0)

    # Union Area
    w1, h1 = b1_x2 - b1_x1, b1_y2 - b1_y1 + eps
    w2, h2 = b2_x2 - b2_x1, b2_y2 - b2_y1 + eps
    union = w1 * h1 + w2 * h2 - inter + eps

    iou = inter / union

    if GIoU or DIoU or CIoU:
        cw = torch.max(b1_x2, b2_x2) - torch.min(b1_x1, b2_x1)  # convex (smallest enclosing box) width
        ch = torch.max(b1_y2, b2_y2) - torch.min(b1_y1, b2_y1)  # convex height
        if CIoU or DIoU:  # Distance or Complete IoU https://arxiv.org/abs/1911.08287v1
            c2 = cw ** 2 + ch ** 2 + eps  # convex diagonal squared
            rho2 = ((b2_x1 + b2_x2 - b1_x1 - b1_x2) ** 2 +
                    (b2_y1 + b2_y2 - b1_y1 - b1_y2) ** 2) / 4  # center distance squared
            if DIoU:
                return iou - rho2 / c2  # DIoU
            elif CIoU:  # https://github.com/Zzh-tju/DIoU-SSD-pytorch/blob/master/utils/box/box_utils.py#L47
                v = (4 / math.pi ** 2) * torch.pow(torch.atan(w2 / (h2 + eps)) - torch.atan(w1 / (h1 + eps)), 2)
                with torch.no_grad():
                    alpha = v / (v - iou + (1 + eps))
                return iou - (rho2 / c2 + v * alpha)  # CIoU
        else:  # GIoU https://arxiv.org/pdf/1902.09630.pdf
            c_area = cw * ch + eps  # convex area
            return iou - (c_area - union) / c_area  # GIoU
    else:
        return iou  # IoU
def countIOU(text,Fname,mergepath2):
    del_index = []                                                                                                                   # correcting the index that need to remove
    same = []                                                                                                                   # correcting the distance that need to remove (it's doesn't used)
    for i in range(len(text)):
        for j in range(i,len(text)):
            if (i != j) and (text["IDcode"][i] != text["IDcode"][j]) and (text["id"][i] == text["id"][j]): 
                box1 =torch.tensor([text["x"][i],text["y"][i],text["x"][i]+text["w"][i],text["y"][i]+text["h"][i]])
                box2 =torch.tensor([text["x"][j],text["y"][j],text["x"][j]+text["w"][j],text["y"][j]+text["h"][j]])                 # Comparing the IDcode , id is the same or not and let i not equal to j
                print(box1)
                print("..........................")
                print(box2)
                iou = bbox_iou(box1,box2)
                if iou >= 0.5:  
                    iou = iou.item()                                                                                                     # if IOU <= 0.5 ,del
                    if text["conf"][i] > text["conf"][j]:                                                                            # Comparing the confidance which is larger                 
                        del_index.append(j)
                    
                    elif text["conf"][j] > text["conf"][i]:
                        del_index.append(i)
                        
                    else:
                        iarea = text["w"][i]*text["h"][i]
                        jarea = text["w"][j]*text["h"][j]
                        area = min([iarea,jarea])
                        if area == iarea:
                            if iarea != jarea:
                                del_index.append(j)
                                
                            else:
                                if (i or j)  not in del_index:
                                 del_index.append(j)   
                        else:
                            if iarea != jarea:
                                del_index.append(i)
             
                            else:
                                if (i or j)  not in del_index:
                                 del_index.append(j) 

                    iarea = text["w"][i]*text["h"][i]
                    jarea = text["w"][j]*text["h"][j]
                    if iarea != jarea :
                        if text["conf"][i] >= text["conf"][j]:
                            same.append(j)
                        else:
                            same.append(i)

    same = sorted(list(set(same)))                    
    del_index = sorted(list(set(del_index)))
    text.drop(text.index[del_index],axis = 0,inplace = True)
    text.to_csv(mergepath2 + "\\" + Fname ,index = 0)                                                                             # del the index
    return del_index,same                                                                                                                 # return index which has been del            

def put_1500csv(model1088path2 = model1088path ,mergepath2 = mergepath):
    Cpath = model1088path2 # first file path
    Clist = glob(Cpath + "\\*.csv")         # all first file path csv
    CHlist = ["id","x","y","w","h","conf","IDcode"]
    count = 0
    tcount = 0
    for i in range(len(Clist)):
        Ctext = pd.read_csv(Clist[i], header=0, names=CHlist)
        Fname = Clist[i].split("\\")[-1]
        text = Ctext
        text = text.reset_index(drop=True)                                  # reset the index
        cf = Fname.split(".")[0]  
        d,s = countIOU(text,Fname,mergepath2)   
        a = len(d)-len(s)   
        if a<0:
            break         
        count += a
        tcount += len(d)                           # for instance : name = img1001
        print(cf)
        print(d)
                                          # Use the function countIOU(text,Fname) or count(text,Fname) 
        print("---------------------------------------------------------------------------------")
    print("del total: " + str(tcount))
    print("del diffient: " + str(count))

def merge():
    f2 = open(resultpath,'w+') # result csv
    files = glob(mergepath+"\*.csv")    # new 1500 csv files
    for file in files:
        name = file.split("\\")[-1]
        name = name.split(".")[0]                           # for instance : name = img1001
        df = pd.read_csv(file,header = 0)
        for i in range(len(df["id"])):
            f2.write(name + "," + str(df["id"][i]) + "," + str(df["x"][i]) + "," + str(df["y"][i]) + "," + str(df["w"][i]) + "," + str(df["h"][i]) + "\n")

    f2.close()



def main():
    put_1500csv()
    merge()


if __name__ == "__main__":
    main()



def final_nms():
    Cpath = r"E:\nopeople_machine\nms\best" # first file path
    Fpath = r"E:\nopeople_machine\nms\car_hov"  # Second file path
    Flist = glob(Fpath + "\\*.csv")  
    Clist = glob(Cpath + "\\*.csv")         # all first file path csv
    CHlist = ["id","x","y","w","h","conf","IDcode"]
    FHlist = ["id","x","y","w","h","conf","IDcode"]
    count = 0
    tcount = 0
    for i in range(len(Clist)):
        Cname = Clist[i].split("\\")[-1]
        Fpath = r"E:\nopeople_machine\nms\car_hov"
        Fpath = Fpath + "\\" + Cname
        dellist = []
        
        try:
            Ftext = pd.read_csv(Fpath, header=0, names=FHlist)
            
            for j in range(len(Ftext["id"])):
                Ftext["IDcode"][j] = Ftext["IDcode"][j] + "F"

                if  (int(Ftext["id"][j]) == 2) or (int(Ftext["id"][j]) ==  3):
                    dellist.append(j)
            Ftext.drop(Ftext.index[dellist],axis = 0,inplace = True)
            
            Ctext = pd.read_csv(Clist[i], header=0, names=CHlist)
            text = pd.concat([Ftext,Ctext],axis=0)
        except:
            Ctext = pd.read_csv(Clist[i], header=0, names=CHlist)
            text = Ctext
            print("except: " + Cname)
        text = text.reset_index(drop=True)                                  # reset the index
        cf = Cname.split(".")[0]  
        d,s = countIOU(text,Cname)   
        a = len(d)-len(s)   
        if a<0:
            break         
        count += a
        tcount += len(d)                           # for instance : name = img1001
        print(cf)
        print(d)
        #print(a)                                      # Use the function countIOU(text,Fname) or count(text,Fname) 
        print("---------------------------------------------------------------------------------")
    print("del total: " + str(tcount))
    print("del diffient: " + str(count))