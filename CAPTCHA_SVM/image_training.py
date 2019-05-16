#-*- coding:utf-8 -*

import numpy as np
import image_process, image_feature, image_model
from config import *
import configparser


#读取配置文件
# config = configparser.ConfigParser()
# config.read("./config.ini")
# captcha_path = config.get("global", "captcha_path") #训练集验证码存放路径
# captcha__clean_path = config.get("global", "captcha__clean_path") #训练集验证码清理存放路径
# train_data_path = config.get("global", "train_data_path") #训练集存放路径
# model_path = config.get("global", "model_path") #模型存放路径
# test_data_path = config.get("global", "test_data_path") #测试集验证码存放路径
#
# image_character_num = config.get("global", "image_character_num") #识别的验证码个数
# threshold_grey = config.get("global", "threshold_grey") #图像粗处理的灰度阈值
# image_width = config.get("global", "image_width") #标准化的图像宽度（像素）
# image_height = config.get("global", "image_height") #标准化的图像高度（像素）





def main():
    # image_process.main() #处理原始验证码，并存到文件
    # feature, label = image_feature.main() #特征处理

    #特征处理
    image_array, image_label = image_feature.read_train_data()     #读入单字符图像
    feature = []
    for num, image in enumerate(image_array):
        feature_vec = image_feature.feature_transfer(image)
        print('label: ',image_label[num])
        #print(feature)
        feature.append(feature_vec)
    print(np.array(feature).shape)
    print(np.array(image_label).shape)

    #训练模型
    result = image_model.trainModel(feature, image_label)




if __name__ == '__main__':
    main()


