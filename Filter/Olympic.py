import numpy as np


def olympic(image, window_size):
    size = window_size // 2

    img = np.pad(image, (size, size), 'constant', constant_values=0)
    res = np.ones(image.shape) * 256

    for i in range(size, img.shape[0] - size):
        for j in range(size, img.shape[1] - size):
            # print(img[i, j])

            kernel = img[i - size:i + size + 1, j - size:j + size + 1]

            # print(kernel)

            kernel = np.reshape(kernel, window_size ** 2)
            kernel.sort()
            olympic_kernel = kernel[1:window_size * window_size - 1]
            mean = np.mean(olympic_kernel)

            # print(mean, "\n")
            res[i - size, j - size] = mean

    return res
