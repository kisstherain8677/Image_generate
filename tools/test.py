import numpy as np
import cv2 as cv

global img
global point1,point2

# 鼠标回调函数
def draw_rec(event,x,y,flags,param):
    global img,point1,point2
    img2=img.copy()#用于显示
    if event == cv.EVENT_LBUTTONDOWN:
        point1=(x,y)
        # cv.circle(img2,point1,10,(0,255,0),5)
        # cv.imshow('image',img2)
    elif event == cv.EVENT_MOUSEMOVE and (flags & cv.EVENT_FLAG_LBUTTON):
        cv.rectangle(img2,point1,(x,y),(255,0,0),2)
        cv.imshow('image',img2)
       # print('x:',x,' y:',y)

    elif event == cv.EVENT_LBUTTONUP:
        point2 = (x, y)
        cv.rectangle(img2,point1,point2,(0,0,255),2)
        cv.imshow('image',img2)
        #截取区域信息
        min_x=min(point1[0],point2[0])
        min_y=min(point1[1],point2[1])
        width=abs(point1[0]-point2[0])
        height=abs(point1[1]-point2[1])



def main():
    global img
    img = np.zeros((512, 512, 3), np.uint8)
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_rec)
    cv.imshow('image', img)
    cv.waitKey(0)

if __name__ =='__main__':
    main()