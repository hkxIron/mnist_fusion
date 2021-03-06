#coding:utf-8
import sys
sys.path.append('/home/hkx/caffe/python')
import caffe

fusion_net = caffe.Net('lenet_fusion_train_val.prototxt', caffe.TEST)

model_list = [
    ('even', 'lenet_even_train_val.prototxt', 'mnist_lenet_even_iter_30000.caffemodel'),
    ('odd', 'lenet_odd_train_val.prototxt', 'mnist_lenet_odd_iter_30000.caffemodel')
]

for prefix, model_def, model_weight in model_list:
    net = caffe.Net(model_def, model_weight, caffe.TEST)
    #将训练好的模型中的参数复制过去
    for layer_name, param in net.params.iteritems():
        n_params = len(param)
        try:
            for i in range(n_params):
                #data[...]是指所有的数据
                fusion_net.params['{}/{}'.format(prefix, layer_name)][i].data[...] = param[i].data[...]
        except Exception as e:
            print(e)

fusion_net.save('init_fusion.caffemodel')
