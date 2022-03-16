import cv2, time
import numpy as np

#codec fourcc
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

# 0 => default camera
cap = cv2.VideoCapture(0)

time.sleep(2)
bg = 0

# for first 60 frames capture the bg
for i in range(60):
    ret, bg = cap.read()

# ret => true/false
# bg => captured frame 

#flipped images
bg = np.flip(bg, axis=1)

# reading everything that's in front of the camera
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)

    # RGB - Red Green Blue
    # HSV - Hue Saturation Value

# 1. Hue: This channel encodes color
# information. Hue can be thought of as
# an angle where 0 degree corresponds
# to the red color, 120 degrees
# corresponds to the green color, and
# 240 degrees corresponds to the blue
# color.
#  2. Saturation: This channel encodes
# the intensity/purity of color. For
# example, pink is less saturated than
# red.
# 3. Value: This channel encodes the
# brightness of color. Shading and
# gloss components of an image
# appear in this channel reading the
# videocapture video.

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # filters = mask_1 and mask_2
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    #bg => if bg has red color, don't hide it
    #img => if img has red color then hide it and put the bg part where red color was.

    #morphing
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)
    # bits 
    # 1 bytes = 8 bits
    # bitwise_not => 1111  => 0000
    # bitwise_and => 1111 AND 1010 => 1010
    # bitwise_or => 1111 OR 1010 => 1111 

    # without red color
    res_1 = cv2.bitwise_and(img, img, mask=mask_2)

    # with red color
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()




