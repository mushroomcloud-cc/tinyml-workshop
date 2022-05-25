# TinyML for Predict Gesture  on ESP32-C3

## 概述
基于6轴传感器数据采样（加速度计和陀螺仪），识别两种手势动作
## 硬件
![image](Images/beetle.jpg)
![image](Images/mu9250.jpg)

## 框架
Tensorflow
Keras
Tensorflow Lite Micro
## 环境
### Python
Python 3.8
Tensorflow
PyOpenGL 

### Arduino
ESP32 Arduino 2.0.3
TensorFlowLite_ESP32 0.9.0

## 设计
### 数据
1.2s 数据长度，采样率 100/s

### 模型
线性全连接网络
720-向量输入，2-向量输出

## 流程
数据采集
预处理
训练
推理应用

## 代码
Host
prediect_gesture