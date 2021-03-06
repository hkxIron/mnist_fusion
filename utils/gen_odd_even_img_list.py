#coding:utf-8
import os
import sys

mnist_path = 'mnist_imgs'
data_sets = ['train', 'val']

for data_set in data_sets:
    odd_list = '{}_odd.txt'.format(data_set)
    even_list = '{}_even.txt'.format(data_set)
    all_list = '{}_all.txt'.format(data_set)
    root = os.sep.join([mnist_path, data_set])
    filenames = os.listdir(root) #show files in dir
    with open(odd_list, 'w') as f_odd, open(even_list, 'w') as f_even, open(all_list, 'w') as f_all:
        for filename in filenames:
            filepath = os.sep.join([root, filename])
            label = int(filename[:filename.rfind('.')].split('_')[1])
            line = '{} {}\n'.format(filepath, label)
            f_all.write(line)

            line = '{} {}\n'.format(filepath, int(label/2))
            #line = '{} {}\n'.format(filepath, int(label/2)) #除以2不是很明白
            #因为对于单独的奇/偶数模型来说就是个五分类问题，所以不需要大于4的label
            if label % 2:
                f_odd.write(line)
            else:
                f_even.write(line)
