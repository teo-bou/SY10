import cv2
import numpy as np

######## Mettre l'image en gris et stocker les valeurs des pixels dans une liste

image_elevation = cv2.imread('C:\\Users\\ellen\\Documents\\UTC\\TC03\\SY10\\projet_sy10\\SY10\\carte_ele_color.png')

image_gray = cv2.cvtColor(image_elevation, cv2.COLOR_BGR2GRAY)

cv2.imshow('Original image',image_elevation)
cv2.imshow('Gray image', image_gray)

values = []

for i in range (image_gray.shape[0]):
    for j in range (image_gray.shape[1]):
        values.append(image_gray[i][j])

print ("Values",values)

cv2.waitKey(0)
cv2.destroyAllWindows()

