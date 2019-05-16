#-*- coding:utf-8 -*


from PIL import Image
import numpy 
import random
import os
import time
import random
import image_training
import configparser
from config import *
import matplotlib.pyplot as plt


def read_captcha(path):
    """
    读取验证码图片
    :param path: 原始验证码存放路径
    :return: image_array, image_label：存放读取的iamge list和label list（图像和标签）
    """
    image_array = []
    image_label = []
    file_list = os.listdir(path)             #获取captcha文件  file_list存储是验证码文件名       
    for file in file_list:
        image = Image.open(path + '/' + file)#打开图片  Image.open的return是class PIL.Image.Image
        file_name = file.split(".")[0]       #获取文件名，此为图像标签
        image_array.append(numpy.array(image))#将图片格式转换为array格式
        image_label.append(file_name)         #image_label是图标签 image_array是图片
        image.close()
    return image_array, image_label


def image_transfer(image_arry,image_label,captcha_clean_save = False):
    """
    图像粗清理
    将图像转换为灰度图像，将像素值小于某个值的点改成白色
    :param image_arry:
    :param captcha_clean_save:
    :return: image_clean:清理过后的图像list
    """
    image_clean = []
    image_change = []
    
    if type(image_arry[0]) == numpy.ndarray:
        for image in image_arry:
            image_change.append(Image.fromarray(image))
    else:
        image_change = image_arry

    for i, image in enumerate(image_change):#enumerate()将一个可遍历的数据对象组合成一个索引序列
        image = image.convert('L')          #转换为灰度图像，即RGB通道从3变为1
        im2 = Image.new("L", image.size, 255)
        #plt.figure("IMAGE")                #用matplotlib画出图像 
        #plt.imshow(image)
        #plt.show()  

        for y in range(image.size[1]):      #遍历所有像素，将灰度超过阈值的像素转变为255（白）;range产生整数列表
            for x in range(image.size[0]):  #range产生0~stop-1的整数
                pix = image.getpixel((x, y))#获得image中(x,y)灰度值
                if int(pix) > threshold_grey:  #灰度阈值 100，这里并不是二值化
                    im2.putpixel((x, y), 255)  #灰度大于100则为白，小于或等于100则保留原值
                else:
                    im2.putpixel((x, y), pix)
        if captcha_clean_save:                 #保存清理过后的iamge到文件
            im2.save(captcha__littleclean_path + '/' + image_label[i] + '.jpg')  
        image_clean.append(im2)
        print("Image processing:the %d pictures."%i)
    return image_clean


def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table



def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    :param img: Image
    :param x:
    :param y:
    :param cur_posi  当前方位，三种情况(待添加) 
    :return:
    """
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum




def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)


def get_clear_bin_image(image):
    """
    图像细清理
    获取干净的二值化的图片。
    图像的预处理：
    1. 先转化为灰度   （没有这步）
    2. 再二值化
    3. 然后清除噪点
    :type img:Image
    :return:
    """
    #imgry = image.convert('L')  # 转化为灰度图

    table = get_bin_table()
    out = image.point(table, '1')  # 转化二值图片:0表示黑色,1表示白色；第一个param表的映射

    noise_point_list = []          # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    for x in range(out.width):
        for y in range(out.height):
            res_9 = sum_9_region(out, x, y)
            if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点((x,y)为黑点，且相邻黑点数小于3
                pos = (x, y)  #获得坐标值
                noise_point_list.append(pos)
    remove_noise_pixel(out, noise_point_list)
    return out


def image_split(image):
    """
    图像切割
    :param image:单幅图像
    :return:单幅图像被切割后的图像list
    """

    #找出每个字母开始和结束的位置
    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = []
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix != True:#找黑点
                inletter = True
        if foundletter == False and inletter == True:#无起点and该列有黑点，该列x为切割起点
            foundletter = True
            start = x
        if foundletter == True and inletter == False:#起点已经找到and该列都是白点，该列x为切割终点,或者找到起点，并且宽度为11时，截至扫描
            foundletter = False
            end = x
            letters.append((start, end))
        elif foundletter == True and (x-start) == split_max_width:
            foundletter = False
            end = x
            letters.append((start, end))
        inletter = False #继续寻找下一个切割起点和终点
    #print(letters)

    # 因为切割出来的图像有可能是噪声点
    # 筛选可能切割出来的噪声点
    subtract_array = [] #存储 结束-开始 值
    for each in letters:
        subtract_array.append(each[1]-each[0])
    reSet = sorted(subtract_array, key=lambda x:x, reverse=True)[0:image_character_num]#sorted排序，参数：迭代对象,x,降序   ？？？
    letter_chioce = []  #存储去除干扰的字符起点终点
    for each in letters:
        if int(each[1] - each[0]) in reSet:
            letter_chioce.append(each)
    # print(letter_chioce)

    #切割图片
    image_split_array = []
    for letter in letter_chioce:
        # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        im_split = image.crop((letter[0], 0, letter[1], image.size[1])) #image.size[1]
        im_split_fullsize=im_split_resize(im_split)
        #im_split = im_split.resize((image_width, image_height))    #图片像素大小转换
        image_split_array.append(im_split_fullsize)
    return image_split_array[0:int(image_character_num)]

#将已经切割的图片大小归一，
def im_split_resize(initial_image):
    #先生成一张白色图片  判断传入图片像素点 如果黑色就令图片为黑
    new_image = Image.new("1", (image_width,image_height), 255)
    if (initial_image.size[0]*initial_image.size[1])>(image_width*image_height):#如果原始图像大小大于image_width*image_height，直接缩小
        initial_image = initial_image.resize((image_width,image_height))
    for y in range(initial_image.size[1]):      #y方向
        for x in range(initial_image.size[0]):  #x方向
            pix = initial_image.getpixel((x, y))#
            if int(pix) == 0:                   #
                new_image.putpixel((x, y), 0)   #
            else:
                new_image.putpixel((x, y), 255)
    return new_image
    #plt.figure("IMAGE")       #用matplotlib画出图像 
    #plt.imshow(new_image)
    #plt.show() 


def image_save(image_array, image_label,save_path):
    """
    保存图像到文件
    :param image_array: 切割后的图像list
    :param image_label: 图像的标签
    :return:
    """
    for num, image_meta in enumerate(image_array):
        file_path = save_path + '/'+image_label[num] + '/'  #切割后图片保存路径
        file_name = str(int(time.time())) + '_' + str(random.randint(0,100)) + '.gif'   #图片文件名
        if not os.path.exists(file_path):   #若文件夹不存在，则创建一个文件夹
            os.makedirs(file_path)

        image_meta.save(file_path  + file_name, 'gif')    
        print("complete save: ",image_label[num])





def main():
    print("The code has run!")
    image_array, image_label = read_captcha(captcha_path)       #读取验证码文件
    print("Begin,rough cleaning!")
    image_clean = image_transfer(image_array,image_label,True)  #验证码图像粗清理

    for k, each_image in enumerate(image_clean):
        image_out = get_clear_bin_image(each_image)             #验证码图像细清理
        image_out.save(captcha__deepclean_path +'/'+ image_label[k]+'.gif', 'gif')
        split_result = image_split(image_out)                   #图像切割
        image_save(split_result, image_label[k],train_data_path)#保存训练图像




if __name__ == '__main__':
    main()


