import cv2
import numpy as np


image = cv2.imread("map.png")  
#image = cv2.resize(image, (336, 550))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
boolean_matrix = binary == 255
print(boolean_matrix.shape)
np.save("boolean_matrix.npy", boolean_matrix)
cv2.imshow("Binary Map", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()