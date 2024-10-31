# 图像描述

## 目录

* [功能介绍](#1)
* [上手指南](#2)
  * [开发前的配置要求](#3)
  * [安装步骤](#4)
* [文件目录说明](#5)

## 功能介绍

本数据处理工具是使用智谱AI视觉大模型进行图像描述，并展示在数加加Pro标注系统。

## 上手指南

### 开发前的配置要求

使用Python的较小版本安装即可，例如：python:3.9-alpine

### 安装依赖包

```
pip install -r requirements.txt
```

## 文件目录说明

```
filetree        
└── code
    ├── Dockerfile ---> 包含再次build的信息
    ├── glm4v_iu.py ---> 图像描述主程序
    ├── log.py ---> 日志模块
    ├── main.py ---> 主函数脚本
    ├── README.md ---> 工具说明
    └── requirements.txt---> 环境安装包信息
```
