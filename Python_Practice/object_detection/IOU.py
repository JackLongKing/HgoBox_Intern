# -*- coding:utf-8 -*-

def IOU(Reframe,GTframe):
    """
    自定义函数，计算两矩形 IOU，传入为均为矩形对角线，（x,y）  坐标。·
    """
    x1 = Reframe[0]
    y1 = Reframe[1]
    width1 = Reframe[2]-Reframe[0]
    height1 = Reframe[3]-Reframe[1]

    x2 = GTframe[0]
    y2 = GTframe[1]
    width2 = GTframe[2]-GTframe[0]
    height2 = GTframe[3]-GTframe[1]

    endx = max(x1+width1,x2+width2)
    startx = min(x1,x2)
    width = width1+width2-(endx-startx)

    endy = max(y1+height1,y2+height2);
    starty = min(y1,y2)
    height = height1+height2-(endy-starty)

    if width <=0 or height <= 0:
        ratio = 0 # 重叠率为 0
    else:
        Area = width*height # 两矩形相交面积
        Area1 = width1*height1
        Area2 = width2*height2
        ratio = Area*1./(Area1+Area2-Area)
    # return IOU
    return ratio,Reframe,GTframe

def get_intersection_over_union(pred,gt):
    x1=pred[0]
    y1=pred[1]
    width1=pred[2]-pred[0]
    height1=pred[3]-pred[1]

    x2=gt[0]
    y2=gt[1]
    width2=gt[2]-gt[0]
    height2=gt[3]-gt[0]

    startx=min(x1,x2)
    endx=max(x1+width1,x2+width2)
    starty=min(y1,y2)
    endy=max(y1+height1,y2+height2)

    width=width1+width2-(endx-startx)
    height=height1+height2-(endy-starty)

    iou=0
    if height<0 or width<0:
        iou=0
    else:
        area=height*width
        area_pred=height1*width1
        area_gt=height2*width2
        iou=area*1.0/(area_gt+area_pred-area)

    return iou

def test_iou():
    examples=[[39, 63, 203, 112], [54, 66, 198, 114],[49, 75, 203, 125], [42, 78, 186, 126],
              [31, 69, 201, 125], [18, 63, 235, 135],[50, 72, 197, 121], [54, 72, 198, 120],
              [35, 51, 196, 110], [36, 60, 180, 108],[3,3,5,5],[8,8,10,10]]
    for i in range(0,len(examples),2):
        # iou,_,_=IOU(examples[i],examples[i+1])
        iou=get_intersection_over_union(examples[i],examples[i+1])
        print("The intersection over union is: ",iou)

if __name__=="__main__":
    test_iou()