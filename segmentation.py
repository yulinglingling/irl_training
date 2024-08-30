import cv2
import numpy as np
import math 
import os
import time

def cal_left(points):
    minx = 0
    id = 0;
    for idx, p in enumerate(points):
        if(p[0] < minx): 
            minx = p[0]
            id = idx;
    nei1 = points[(4 + id - 1) % 4]
    nei2 = points[(4 + id + 1) % 4]
    if math.sqrt((nei1[0] - points[id][0]) ** 2 + (nei1[1] - points[id][1]) ** 2) > math.sqrt((nei2[0] - points[id][0]) ** 2 + (nei2[1] - points[id][1]) ** 2):
        if(points[id][1] > nei1[1]):
            return nei1, points[id]
        else:
            return points[id], nei1 
    else:
         if(points[id][1] > nei2[1]):
            return nei2, points[id]
         else:
            return points[id], nei2  
def cal_right(points):
    maxx = 0
    id = 0;
    for idx, p in enumerate(points):
        if(p[0] > maxx): 
            maxx = p[0]
            id = idx;
    nei1 = points[(4 + id - 1) % 4]
    nei2 = points[(4 + id + 1) % 4]
    if math.sqrt((nei1[0] - points[id][0]) ** 2 + (nei1[1] - points[id][1]) ** 2) > math.sqrt((nei2[0] - points[id][0]) ** 2 + (nei2[1] - points[id][1]) ** 2):
        if(points[id][1] > nei1[1]):
            return nei1, points[id]
        else:
            return points[id], nei1 
    else:
         if(points[id][1] > nei2[1]):
            return nei2, points[id]
         else:
            return points[id], nei2  
def empty(v):
    pass

    # 读取图像并调整大小
def segmentation():
    img_orbbec = cv2.imread('captured_images/captured_photo.jpg')
    img_brio = cv2.imread('captured_images/brio.jpg')
        # 转换为 HSV 色彩空间
    hsv_orbbec = cv2.cvtColor(img_orbbec, cv2.COLOR_BGR2HSV)
    hsv_brio = cv2.cvtColor(img_brio, cv2.COLOR_BGR2HSV)

        # 创建一个窗口和滑块
    # cv2.namedWindow('trackbar')
    # cv2.resizeWindow('trackbar', 1280, 720)

    # cv2.createTrackbar('hue min', 'trackbar', 0, 179, empty)
    # cv2.createTrackbar('hue max', 'trackbar', 179, 179, empty)
    # cv2.createTrackbar('sat min', 'trackbar', 0, 255, empty)
    # cv2.createTrackbar('sat max', 'trackbar', 255, 255, empty)
    # cv2.createTrackbar('val min', 'trackbar', 0, 255, empty)
    # cv2.createTrackbar('val max', 'trackbar', 255, 255, empty)


    # # while True:
    #     # 获取滑块的值
    # h_min = cv2.getTrackbarPos('hue min', 'trackbar')
    # h_max = cv2.getTrackbarPos('hue max', 'trackbar')
    # s_min = cv2.getTrackbarPos('sat min', 'trackbar')
    # s_max = cv2.getTrackbarPos('sat max', 'trackbar')
    # v_min = cv2.getTrackbarPos('val min', 'trackbar')
    # v_max = cv2.getTrackbarPos('val max', 'trackbar')

        # 创建 HSV 颜色范围
    # lower = np.array([h_min, s_min, v_min])
    # upper = np.array([h_max, s_max, v_max])

    # lower = np.array([105, 105, 38])
    # upper = np.array([109, 230, 238])
    lower = np.array([105, 105, 12])
    upper = np.array([120, 255, 238])

    low_brio = np.array([103, 210, 57])
    up_brio = np.array([110, 255, 222])

        # 创建掩码
    mask = cv2.inRange(hsv_orbbec, lower, upper)
    mask_brio = cv2.inRange(hsv_brio, low_brio, up_brio)

        # 应用形态学操作以去除噪声
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 关闭操作
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 打开操作

    mask_brio = cv2.morphologyEx(mask_brio, cv2.MORPH_CLOSE, kernel)  # 关闭操作
    mask_brio = cv2.morphologyEx(mask_brio, cv2.MORPH_OPEN, kernel)   # 打开操作

        # 创建一个感兴趣区域 (ROI) 掩码
    roi_mask = np.zeros_like(mask)
    roi_x, roi_y, roi_w, roi_h = 150, 0, 980, 720  # 定义 ROI 区域 (x, y, width, height)
    roi_mask[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = 255  # 设置 ROI 区域为白色

        # 将 ROI 掩码应用到形态学处理后的掩码上
    mask = cv2.bitwise_and(mask, roi_mask)

        # 查找轮廓并绘制最小外接矩形
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = img_orbbec.copy()
    tour_brio, _ = cv2.findContours(mask_brio, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_tour_brio = img_brio.copy()
        
    maxarea = 0;
    maxbox = 0;
    maxpoints = [0, 0];
    for contour in contours:
            # 获取每个轮廓的最小外接矩形
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            # 绘制最小外接矩形
            cv2.drawContours(img_contours, [box], 0, (0, 255, 0), 2)
            
            # 打印矩形坐标
            # print(f'Rectangle Points: {box}')

            # 获取矩形的宽度和高度
            width = rect[1][0]
            height = rect[1][1]
            print("width:", width, "height:", height)
            tmppoints = []
            if(width > height): 
                # if(box[0][1] < box[3][1]):
                    tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
                    tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                # else:
                #     tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                #     tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
            else:
                # if(box[0][1] < box[3][1]):
                #     tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
                #     tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                # else:
                    tmppoints.append([(box[0][0] + box[3][0]) / 2, (box[0][1] + box[3][1]) / 2]);
                    tmppoints.append([(box[1][0] + box[2][0]) / 2, (box[1][1] + box[2][1]) / 2]);
            # 计算面积
            area = width * height
            if(area > maxarea): 
                maxarea = area;
                maxbox = box;
    left_p, right_p = 0, 0
    if(type(maxbox) != int):
        left_p = cal_left(maxbox)
        right_p = cal_right(maxbox)
        maxpoints[0] = (left_p[0][0] + right_p[0][0]) / 2, (left_p[0][1] + right_p[0][1]) / 2;
        maxpoints[1] = (left_p[1][0] + right_p[1][0]) / 2, (left_p[1][1] + right_p[1][1]) / 2;
    else: 
        print("orbbec box not found")
        return None

    maxarea = 0;
    maxbox_brio = 0;
    maxpoints_brio = [0, 0];
    for contour in tour_brio:
            # 获取每个轮廓的最小外接矩形
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            # 绘制最小外接矩形
            cv2.drawContours(img_tour_brio, [box], 0, (0, 255, 0), 2)
            
            # 打印矩形坐标
            # print(f'Rectangle Points: {box}')

            # 获取矩形的宽度和高度
            width = rect[1][0]
            height = rect[1][1]
            # print("width:", width, "height:", height)
            tmppoints = []
            if(width > height): 
                # if(box[0][1] < box[3][1]):
                    tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
                    tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                # else:
                #     tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                #     tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
            else:
                # if(box[0][1] < box[3][1]):
                #     tmppoints.append([(box[3][0] + box[2][0]) / 2, (box[3][1] + box[2][1]) / 2]);
                #     tmppoints.append([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2]);
                # else:
                    tmppoints.append([(box[0][0] + box[3][0]) / 2, (box[0][1] + box[3][1]) / 2]);
                    tmppoints.append([(box[1][0] + box[2][0]) / 2, (box[1][1] + box[2][1]) / 2]);
            # 计算面积
            area = width * height
            if(area > maxarea): 
                maxarea = area;
                maxbox_brio = box;
    left_brio, right_brio = 0, 0
    if(type(maxbox_brio) != int): 
        left_brio = cal_left(maxbox_brio)
        right_brio = cal_right(maxbox_brio)
        maxpoints_brio[0] = (left_brio[0][0] + right_brio[0][0]) / 2, (left_brio[0][1] + right_brio[0][1]) / 2;
        maxpoints_brio[1] = (left_brio[1][0] + right_brio[1][0]) / 2, (left_brio[1][1] + right_brio[1][1]) / 2;
    else: 
        print("mx brio box not found")
        return None

    # print("orbbec max box", maxbox)
    
    # print("pen vector", maxpoints[1][0] - maxpoints[0][0], maxpoints[1][1] - maxpoints[0][1])
    
    # print("orbbec high", maxpoints[0])
    # print("orbbec low", maxpoints[1])

    # print("brio maxbox", maxbox_brio)
    # print("brio high", maxpoints_brio[0])
    # print("brio low", maxpoints_brio[1])

        # 显示结果
    # cv2.imshow('contours', img_contours)
    # cv2.imshow('contour brio', img_tour_brio)
    # cv2.waitKey(0)
    cv2.imwrite('captured_images/orbbec.jpg', img_contours)
    cv2.imwrite('captured_images/mx_brio.jpg', img_tour_brio)
        
    cv2.destroyAllWindows()
    print("left orbbec, mid brio, mid orbbec, right, brio", left_p, maxpoints_brio, maxpoints, right_brio)
    return left_p, maxpoints_brio, maxpoints, right_brio

if(__name__ == '__main__'):
    segmentation()








