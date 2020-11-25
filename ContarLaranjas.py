import cv2
import numpy as np

myColors = [ 
    [ 0, 209, 164, 21, 255, 255], # Imagem 1
]

def preProcessImage(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)

    kernel = np.ones((5, 5))

    imgDilate = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDilate, kernel, iterations=1)
    
    return imgCanny

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    counter = 0
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if (area > 100):
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            counter+=1

    return x+w//2, y, counter

def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    for index, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
    
        mask = cv2.inRange(imgHSV, lower, upper)

        x, y, counter = getContours(mask)

        if counter != 0:

            cv2.putText(imgContour, f'Quantidade: {counter}', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

        # cv2.circle(imgContour, (x, y), 10, (255, 0, 0), cv2.FILLED)

        if x != 0 and y != 0:
            newPoints.append([x, y, index])

        #cv2.imshow(str(color[0]), mask)
    return newPoints, counter

while True:
    img = cv2.imread("../Datasets/Laranjas/p/laranja.jpg")

    cv2.resize(img, (480, 640))

    imgContour = img.copy()
    
    # imgThres = preProcessImage(img)
    newPoints = findColor(img, myColors)

    cv2.imshow("Original", img)
    cv2.imshow("Contorno", imgContour)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()