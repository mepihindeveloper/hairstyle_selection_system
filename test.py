import numpy as np
import cv2

def show(index):
    face_img = cv2.imread("client/tmp_images/temp.png", -1)
    hair_image = cv2.imread('server/hairstyle_images/women/%i.png' % (index + 1), -1)
    blank_image = np.zeros((hair_image.shape), np.uint8)
    blank_image = cv2.resize(blank_image, (hair_image.shape[1]*2, hair_image.shape[0]*2))

    face_offset_y = int(face_img.shape[0] / 2 - face_img.shape[0] / 5)

    y_offset = int((blank_image.shape[0] / 2) - (face_img.shape[0] / 2)) - face_offset_y
    x_offset = int((blank_image.shape[1] / 2) - (face_img.shape[1] / 2))

    blank_image[
        y_offset: y_offset + face_img.shape[0],
        x_offset: x_offset + face_img.shape[1]
    ] = face_img

    x_offset = int(
        (blank_image.shape[1] / 2) - (hair_image.shape[1] / 2)
    )
    y_offset = 0

    y1, y2 = y_offset, y_offset + hair_image.shape[0]
    x1, x2 = x_offset, x_offset + hair_image.shape[1]

    alpha_s = hair_image[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        blank_image[
            y1:y2,
            x1:x2,
            c
        ] = (alpha_s * hair_image[:, :, c] + alpha_l * blank_image[y1:y2, x1:x2, c])

    cv2.imshow("s", blank_image)
    cv2.imwrite("%i.png" % (index + 1),blank_image)
    cv2.waitKey()

for i in range(10):
    show(i)