import cv2
import numpy as np
 
# Stack method to join multiple images
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
# Function to find the outer Corners of shape
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  # finding contours
    for cnt in contours:
        area = cv2.contourArea(cnt) # calculating area of shapes
        print(area)
        if area > 500:  # if we want to draw contours only to those shapes which have area greater than 500
            cv2.drawContours(imgContours,cnt,-1,(255,0,0),1) # drawing contours 
            peri = cv2.arcLength(cnt,True)  # to find the parameter of shapes , True is used because shape is closed.
            print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            objCor = len(approx)  # number of object corner
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3: objectType ="Tri"
            else: objectType="None"

            cv2.rectangle(imgContours,(x,y),(x+w,y+h),(0,225,0),2) # Creating rectangle arround the shapes
            cv2.putText(imgContours,objectType,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,255,2))
 


img=cv2.imread("Resources/shapes2.png")
imgContours = img.copy() # copy img to imgContours

imgGrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGrey,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
imgBlack = np.zeros_like(img)
getContours(imgCanny) # Calling getContours function


imgStack = stackImages(0.6,([img,imgGrey,imgBlur],
                                [imgCanny,imgContours,imgBlack]))
cv2.imshow("Stack Image",imgStack)
cv2.waitKey(0)