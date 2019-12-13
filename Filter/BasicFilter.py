

import numpy as np
import math


class Filtering:
    image = None
    filter = None
    cutoff = None
    order = None

    def __init__(self, image, filter_name, cutoff, order=0):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        order: the order of the filter (only for butterworth
        returns"""
        self.image = image
        if filter_name == 'ideal_l':
            self.filter = self.get_ideal_low_pass_filter
        elif filter_name == 'ideal_h':
            self.filter = self.get_ideal_high_pass_filter
        elif filter_name == 'butterworth_l':
            self.filter = self.get_butterworth_low_pass_filter
        elif filter_name == 'butterworth_h':
            self.filter = self.get_butterworth_high_pass_filter
        elif filter_name == 'gaussian_l':
            self.filter = self.get_gaussian_low_pass_filter
        elif filter_name == 'gaussian_h':
            self.filter = self.get_gaussian_high_pass_filter

        self.cutoff = cutoff
        self.order = order

    def get_ideal_low_pass_filter(self, shape, cutoff):
        print("I made it to ideal low function")
        rows = shape[0]
        cols = shape[1]

        filtered_image = np.ones((rows, cols))
        p = rows
        q = cols
        for row in range(rows):
            for col in range(cols):
                distance = np.sqrt((np.power(row - (p/2), 2) + np.power(col - (q/2), 2)))
                #   D_0 IS CUTOFF
                if distance <= cutoff:
                    filtered_image[row, col] = 1
                else:
                    filtered_image[row, col] = 0

        return filtered_image

    def get_ideal_high_pass_filter(self, shape, cutoff):

        low_pass_class = Filtering(self.image, 'ideal_l', self.cutoff)
        ideal_low = low_pass_class.filtering()
        filtered_image = 1 - ideal_low

        return filtered_image

    def get_butterworth_low_pass_filter(self, shape, cutoff, order):

        rows, cols = shape

        filtered_image = np.ones((rows, cols))
        p = rows
        q = cols
        for row in range(rows):
            for col in range(cols):
                distance = np.sqrt(np.power(row - p / 2, 2) + np.power(col - q / 2, 2))
                filtered_image[row, col] = 1 / (1 + (np.power(distance / cutoff, 2 * order)))
        return filtered_image

    def get_butterworth_high_pass_filter(self, shape, cutoff, order):

        low_pass_class = Filtering(self.image, 'butterworth_l', self.cutoff, self.order)
        butterworth_low = low_pass_class.filtering()
        filtered_image = 1 - butterworth_low

        return filtered_image

    def get_gaussian_low_pass_filter(self, shape, cutoff):

        rows, cols = shape
        filtered_image = np.zeros((rows, cols))

        p = rows
        q = cols

        for row in range(rows):
            for col in range(cols):
                distance = np.sqrt(np.power(row - p / 2, 2) + np.power(col - q / 2, 2))
                filtered_image[row, col] = np.exp(-distance ** 2 / (2 * (cutoff ** 2)))

        return filtered_image

    def get_gaussian_high_pass_filter(self, shape, cutoff):

        low_pass_class = Filtering(self.image, 'gaussian_l', self.cutoff)
        gaussian_low = low_pass_class.filtering()
        filtered_image = 1 - gaussian_low

        return filtered_image

    def get_homomorphic_filter(self, shape, cutoff, order):
        a = 0.75
        b = 1.25

        rows, cols = shape
        filtered_image = np.zeros((rows, cols))

        p = rows
        q = cols

        for row in range(rows):
            for col in range(cols):
                distance = np.sqrt(np.power(row - p / 2, 2) + np.power(col - q / 2, 2))
                filtered_image[row, col] = 1 - (1 / (distance / cutoff) ** (2 * order))

    def post_process_image(self, image):

        image = (image - np.min(image)) * (255 / (np.max(image) - np.min(image)))

        return image

    def filtering(self):

        img = self.image.copy()
        # COMPUTE DFT
        dft_img = np.fft.fft2(img)
        # SHIFT DFT TO CENTER
        shft_dft_img = np.fft.fftshift(dft_img)
        # PERFORM LOG COMPRESSION
        mag_fil_dft = np.log(np.abs(shft_dft_img))
        # APPLY CONTRAST STRETCH
        mag_fil_dft = (255 * (mag_fil_dft / np.max(mag_fil_dft))).astype('uint8')

        #  CHECK IF FILTER HAS ORDER
        if self.order is 0:
            mask = self.filter(self.image.shape, self.cutoff)
        else:
            mask = self.filter(self.image.shape, self.cutoff, self.order)

        #   SHIFTED DFT * MASK
        filtered_dft_img = shft_dft_img * mask
        #   CONVOLUTION THEOREM
        filter_output = mag_fil_dft * mask

        #   INVERSE DFT
        inv_shift_img = np.fft.ifftshift(filtered_dft_img)
        inv_dft_shft_img = np.fft.ifft2(inv_shift_img)

        #------CONVERT IMAGES-------#
        #   FILTERED IMAGE
        fil_image = np.abs(inv_dft_shft_img)
        fil_image = self.post_process_image(fil_image)

        return fil_image


def PSNR(image, image_filtered):
    print("---------EXECUTING PSNR-------")
    MSE = 0
    # image = cv2.imread(r"output/Lenna0.jpg", 0)

    size = image.shape[0] * image.shape[1]

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #         print("image- 1",image[i,j])
            #         print(image_new[i,j])
            MSE += (((image[i, j] - image_filtered[i, j]) ** 2) / size)
    print("MSE: ", MSE)
    R = 256
    PSNR = 10 * math.log10((R ** 2) / MSE)
    return PSNR
