import numpy as np
import cv2
import math

input_image = cv2.imread("lenna.jpg", 0)


def HomomorphicFilter(image,cutoff):
    c = 0.5 #Constant to control sharpness of slope of filter while transitioning from yL to yH
    yL = 0.5  #Usually yL < 1
    yH = 2  #Usually yH > 1, tends to decrease contribution by low frequencies(Illumination) and increase contribution made by high frequencies(reflectance)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 0:
                image[i, j] = 1
    log_of_img = np.log(image)  #Apply Log to seperate out illumination and reflectance
    print(image)
    print('******************************************************************')
    print(log_of_img)
    fft_image = np.fft.fft2(log_of_img) #Applying Fourier Transform on the log image
    # someimg = np.abs(fft_image)
    fft_shift = np.fft.fftshift(fft_image)  #Applying shift to center low frequencies
    mask = np.zeros((image.shape[0], image.shape[1]))
    # print(mask)
    Pby2 = mask.shape[0] / 2
    Qby2 = mask.shape[1] / 2
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            D_u_v = ((i - Pby2) ** 2 + (j - Qby2) ** 2) ** 0.5
            mask[i, j] = (yH-yL)*(1 - math.exp((-c*(D_u_v ** 2)) / (cutoff ** 2))) + yL;   #Getting the Homorphic Filter

    filter_image = fft_shift * mask # Applying the filter operation
    Inv_fft_shift = np.fft.ifftshift(filter_image)  #Inverse Shifting the image
    ifft_image = np.fft.ifft2(Inv_fft_shift)    #Converting to Spatial domain by applying Inverse fourier transform
    mag_filter_image = np.abs(ifft_image) # Computing the magnitude in spatial domain

    b = np.max(mag_filter_image)
    a = np.min(mag_filter_image)
    for i in range(mag_filter_image.shape[0]):
        for j in range(mag_filter_image.shape[1]):
            mag_filter_image[i, j] = (mag_filter_image[i, j] - a) * (255 / (b - a)).astype('uint8')
    mag_filter_image = np.exp(mag_filter_image)
    return mag_filter_image

homo_image = HomomorphicFilter(input_image,75)


def display_image(homo_image):
    """A function to display image"""
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    ims = cv2.resize(homo_image, (960, 540))
    cv2.imshow("img", ims)
    cv2.waitKey(0)
    # cv2.imwrite("homo_image", homo_image)
display_image(input_image)
display_image(homo_image)