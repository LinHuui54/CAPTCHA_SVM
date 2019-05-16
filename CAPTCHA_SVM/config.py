#-*- coding:utf-8 -*



#原始路径
path = 'C:/Users/Administrator/Desktop/GraduationProject/captcha_ml'
#训练集原始验证码文件存放路径
captcha_path = path + '/data/Captcha' #测试模式数据captcha_thin，正常模式数据Captcha
#训练集验证码粗清理存放路径
captcha__littleclean_path = path + '/data/captcha_little_clean'
#训练集验证码细清理存放路径
captcha__deepclean_path = path + '/data/captcha_deep_clean'
#训练集存放路径
train_data_path = path + '/data/training_data'
#模型存放路径
model_path = path + '/mymodel/SVM_linear_model.pkl'#mymodel
#测试集原始验证码文件存放路径
test_data_path = path + '/data/test_data'#path + '/data/test_data'
#测试结果存放路径
output_path = path + '/result/result.txt'

#识别的验证码个数
image_character_num = 4

#图像粗处理的灰度阈值
threshold_grey = 100

#限制切割最大宽度
split_max_width = 13

#标准化的图像大小
image_width = 11
image_height = 26


