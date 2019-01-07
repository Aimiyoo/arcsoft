# Arcsoft

http://www.arcsoft.com.cn/index.html  
由于官网提供的demo是c语言版本的，使用起来不怎么友好。于是，该项目按照官网提供的c版本demo，基于python3，实现了人脸检测，年龄，性别识别功能。  


## Dependencies
1. Python3
2. pillow
3. arcsoft sdk 1.11
4. app id和key

## Deploy

整个项目目录结构如structure.png所示：

1. pip install -r requirements
2. 去arcsoft官网申请sdk以及sdk对应的key（完全免费无限制）
3. 将下载好的sdk放到sdk目录下
4. 将申请的app id以及key填写到conf/config.ini

## Run

```bash
python my_face.py
```

## Comparison

人脸检测做的比较好的有face++，感兴趣的可以去face++官网申请使用

1. 质量  
和face++的人脸检测做了对比，发现识别效果差不多，并没有明显区别（极端情况除外，侧脸角度特别大的话，arcsoft识别不到人脸，face++还可以正常识别）。  
2. 速度  
arcsoft是离线sdk，速度上比face++快了1-2个数量级，并且qps没有限制（face++只提供API服务，qps有限制，个人qps是2，企业版是10）。  


## Instruction

1. 官网提供的sdk有两个版本，1.11和2.0，两个版本的使用有区别，该项目所用的版本是1.11
2. face_detect.py是人脸检测的代码，年龄、性别、人脸对比等功能均基于人脸检测，所以将该功能单独封装成一个文件
3. 该项目只现实了人脸检测，年龄，性别功能，其他功能如人脸对比没有实现，有需求的可以仿照代码自己实现
4. 该项目在linux x64，python3环境下测试没有问题，windows环境下可能需要稍微改造，有需求的可以仿照代码自己实现



