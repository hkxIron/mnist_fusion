#coding:utf-8
import pickle
import gzip
import numpy as np
from PIL import Image

"""
将图像以砖块的形式显示出来
"""

def load_data():
    with gzip.open('./mnist.pkl.gz') as fp:
        training_data, valid_data, test_data = pickle.load(fp)
    return training_data, valid_data, test_data


    #------------

def normalize(darr, eps=1e-8):
    # normalize(x) = (x-min)/(max-min)
    darr -= darr.min()
    darr *= 1./(darr.max()+eps)
    return darr

def tile_raster_images(X, image_shape, tile_shape, 
    tile_spacing=(0, 0), normalize_rows=True, output_pixel_vals=True):
    # image_shape：每一个砖的高和宽，
    # tile_shape：在横纵两个方向上分别有多少砖
    # tile_spacing：砖与砖之间的距离
    # normalize_rows：是否对砖进行归一化
    # output_pixel_vals：是否对砖以图像的形式进行显示

    assert len(image_shape) == 2
    assert len(tile_shape) == 2
    assert len(tile_spacing) == 2
    # 对参数进行断言，确保它们都是二维元组
    output_shape = [
        (ishp + tsp)*tshp-tsp
        for ishp, tshp, tsp in zip(image_shape, tile_shape, tile_spacing)
    ]
    # image_shape == (28, 28)   mnist data
    # tile_shape == (10, 10), tile_spacing == (1, 1)
    # [(28+1)*10-1]*[(28+1)*10-1]                   

    H, W = image_shape
    Hs, Ws = tile_spacing
    dt = 'uint8' if output_pixel_vals else X.dtype
    # python 风格的三目运算符
    output_array = np.zeros(output_shape, dtype=dt)

    # 开始贴砖
    for i in range(tile_shape[0]):
        for j in range(tile_shape[1]):
            if i*tile_shape[1]+j < X.shape[0]:
                # X的每一行是一个图像（二维）flatten后的（一维的行向量）
                this_x = X[i*tile_shape[1]+j]
                this_image = normalize(this_x.reshape(image_shape)) if normalize_rows else this_x.reshape(image_shape)
                c = 255 if output_pixel_vals else 1
                output_array[
                    i*(H+Hs):i*(H+Hs)+H, j*(W+Ws):j*(W+Ws)+W
                ] = this_image*c
    return output_array


def main():
    training_data, valid_data, test_data = load_data()
    # training_data, valid_data, test_data 均是二元 tuple
    # tuple of ndarray：feature and label
                
    print "train data size:",training_data[0].shape
    print "train label size:",training_data[1].shape
    I = training_data[0][0]
    I.resize((28, 28))
    im = Image.fromarray((I*256).astype('uint8'))
    im.show()
    #--------------
    #X = numpy.random.randn(500, 28*28)
    X = training_data[0][0:500]
    arr = tile_raster_images(X, image_shape=(28, 28), 
                tile_shape=(12, 12), tile_spacing=(1, 1))
    img = Image.fromarray(arr)
    img.show()
    img.save('./mnist_tiles.png')
    # 这里也可使用 matplotlib 进行显示
    # plt.imshow(img, cmap='gray')
    # plt.show()

if __name__ == '__main__':
    main()
