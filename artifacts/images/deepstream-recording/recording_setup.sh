#!/bin/bash

# from deepstream-test5
cd /opt/nvidia/deepstream/deepstream-7.0
apt-get install -y \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    libgstrtspserver-1.0-dev \
    libx11-dev \
    libjson-glib-dev \
    libyaml-cpp-dev

# from /opt/nvidia/deepstream/deepstream/sources/libs/kafka_protocol_adaptor
cd /opt/nvidia/deepstream/deepstream-7.0
git clone https://github.com/confluentinc/librdkafka.git
cd librdkafka
git checkout tags/v2.2.0

# --enable-ssl
./configure
make
make install
cp /usr/local/lib/librdkafka* /opt/nvidia/deepstream/deepstream/lib/
ldconfig

apt-get install -y \
    libglib2.0 \
    libglib2.0-dev \
    libjansson4 \
    libjansson-dev \
    libssl-dev \ 
    protobuf-compiler
    
# from deepstream-test5
cd /opt/nvidia/deepstream/deepstream-7.0/sources/apps/sample_apps/deepstream-test5
export CUDA_VER=12.2
make

# cd /opt/nvidia/deepstream/deepstream-7.0
# git clone https://github.com/WongKinYiu/yolov7.git
# git clone https://github.com/marcoslucianops/DeepStream-Yolo
# cd /opt/nvidia/deepstream/deepstream-7.0/yolov7
# pip3 install -r requirements.txt
# pip3 install onnx onnxsim onnxruntime

# cd /opt/nvidia/deepstream/deepstream-7.0/DeepStream-Yolo
# CUDA_VER=12.2 make -C nvdsinfer_custom_impl_Yolo

# # convert model
# cd /opt/nvidia/deepstream/deepstream-7.0/yolov7
# cp ../DeepStream-Yolo/utils/export_yoloV7.py .
# wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt
# python3 export_yoloV7.py -w yolov7.pt --dynamic
# cp labels.txt ../DeepStream-Yolo
# cp yolov7.onnx ../DeepStream-Yolo

# cd /opt/nvidia/deepstream/deepstream-7.0/sources/apps/sample_apps/deepstream-test5

# # move artifacts from DeepStream-YOLO repository to deepstream-test5
# cp /opt/nvidia/deepstream/deepstream-7.0/DeepStream-Yolo/config_infer_primary_yoloV7.txt .
# cp /opt/nvidia/deepstream/deepstream-7.0/DeepStream-Yolo/labels.txt .
# cp /opt/nvidia/deepstream/deepstream-7.0/DeepStream-Yolo/yolov7.onnx .
# cp -r /opt/nvidia/deepstream/deepstream-7.0/DeepStream-Yolo/nvdsinfer_custom_impl_Yolo/ .

echo -n \"--------------FINISHED--------------\"