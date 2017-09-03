#!/usr/bin/env sh
set -e

#./build/tools/caffe train --solver=examples/mnist/lenet_solver.prototxt $@
#${CAFFE_HOME}/build/tools/caffe train --solver=../../examples/mnist/lenet_solver.prototxt $@
cd /home/hkx/windata/mnist/
nohup ${CAFFE_HOME}/build/tools/caffe train \
    --solver=lenet_fusion_solver.prototxt \
    --weights=init_fusion.caffemodel \
    $@ >&1|tee log/log_train_lenet_even
