#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# GUI_captcha_predict.py

import image_predict
import image_process
import wx 
from PIL import Image
import os
import io
import queue
import numpy
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from config import *

image_queue = queue.Queue()

def PilImg2WxImg(pilImg):  
    '''''PIL的image转化为wxImage'''
    image = wx.EmptyImage(pilImg.size[0],pilImg.size[1])  
    image.SetData(pilImg.convert("RGB").tostring())  
    #image.SetAlpha(pilImg.convert("RGBA").tostring()[3::4])
    #use the wx.Image or convert it to wx.Bitmap  
    #bitmap = wx.BitmapFromImage(image)  
    return image 

class Example(wx.Frame):
   
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(800, 700))
             
        self.InitUI()
        self.Centre()
        self.Show()     
         
    def InitUI(self):
     
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#ec6091')  #set背景色  #fa897b
        #静态文字显示
        font_name = wx.Font(12, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_LIGHT)#创建文字格式 无加粗
        font_title = wx.Font(13,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD) #加粗文字格式
        des_name = wx.StaticText(panel, label='题目：基于机器学习的验证码识别',pos = (10,10)) #显示名字
        des_name.SetFont(font_title)                                                    #设置该文字格式 
        stu_name = wx.StaticText(panel, label='学    生：林 辉',pos = (10,40))
        stu_name.SetFont(font_name)
        tea_name = wx.StaticText(panel, label='指导老师：汪茂稳',pos = (10,70))
        tea_name.SetFont(font_name)
        #添加按键
        open_pic_butt = wx.Button(panel, label="打开图像", size=(90, 28),pos = (50,150))
        pic_pretreat_butt = wx.Button(panel, label="图像预处理", size=(90, 28),pos = (50,150+80))
        deep_treat_butt = wx.Button(panel, label="深度处理并切割", size=(120, 28),pos = (35,150+160))
        cap_iden_butt = wx.Button(panel, label="验证码识别", size=(120, 28),pos = (35,150+240))
        #按键事件设置
        self.Bind(wx.EVT_BUTTON, self.Open_pic_event, open_pic_butt)     #事件绑定器wx.EVT_BUTTON
        self.Bind(wx.EVT_BUTTON,self.Pic_pretreat_event,pic_pretreat_butt)
        self.Bind(wx.EVT_BUTTON,self.Pic_deeptreat_event,deep_treat_butt)
        self.Bind(wx.EVT_BUTTON,self.Pic_iden_event,cap_iden_butt)


    #打开图像事件
    def Open_pic_event(self,event):
        print("start reading")
        filesFilter =  "All files (*.*)|*.*"    #文件格式
        fileDialog = wx.FileDialog(self, message ="选择单个文件", wildcard = filesFilter, style = wx.FD_OPEN|wx.FD_MULTIPLE)
        dialogResult = fileDialog.ShowModal()
        path = fileDialog.GetPath()
        if ".jpg" in path:      #判断是否是图像
            wx_cap_image = wx.Image(path, wx.BITMAP_TYPE_JPEG) #载入wx格式验证码
            pil_cap_image = Image.open(path)
            #plt.figure("IMAGE")       #用matplotlib画出图像 
            #plt.imshow(pil_cap_image)
            #plt.show()  
            w = wx_cap_image.GetWidth() #读取验证码图像的宽和高
            h = wx_cap_image.GetHeight()
            if w ==80 and h == 26:   #判断是否是验证码
                dis_cap_image = wx_cap_image.Scale(w*3,h*3)   #放大验证码
                wx.StaticBitmap(self, -1, wx.BitmapFromImage(dis_cap_image),pos = (350,50))#显示验证码
                image_queue.put(pil_cap_image)      #将pil_cap_image载入队列，等待下一步读入处理
                #print(path)
                #return cap_image     #返回读取的图像
            else:
                print('error!') #用一个Dialog类
        else:
            print('error!')

    #图像预处理
    def Pic_pretreat_event(self,event):
        #if image_queue.empty() == True:
            #print("The queue is empty.")
            #return None
        cap_image = []                       
        cap_image.append(image_queue.get())   #读队列  需要判断队列有没有信息     是 PIL.Image类型  
        image_clean = image_process.image_transfer(cap_image,'image_predict.jpg')
        image_queue.put(image_clean[0])
        #plt.figure("IMAGE")       #用matplotlib画出图像 
        #plt.imshow(image_clean[0])
        #plt.show()  
        wx_clean_image = PilImg2WxImg(image_clean[0])       #将PilIMG类型转换为WxIMG类型
        w = wx_clean_image.GetWidth()                       #读取验证码图像的宽和高
        h = wx_clean_image.GetHeight()
        dis_clean_image = wx_clean_image.Scale(w*3,h*3)
        wx.StaticBitmap(self, -1,wx.BitmapFromImage(dis_clean_image),pos = (350,200))
    
    #图像深度处理，并切割
    def Pic_deeptreat_event(self,event):
        image_array = []
        wx_split_image = []
        dis_split_image = []
        cap_image = image_queue.get()
        image_out = image_process.get_clear_bin_image(cap_image) #转换为二值图片，并去除剩余噪声点
        plt.figure("IMAGE")       #用matplotlib画出图像 
        plt.imshow(image_out)
        plt.show() 
        split_result = image_process.image_split(image_out) #切割图片
        image_queue.put(split_result)       #将切割结果载入队列
        #将四张单字符图像转换格式并一一显示
        for k,image in enumerate(split_result):    
            wx_split_image.append(PilImg2WxImg(image))       #将PilIMG类型转换为WxIMG类型
            w = wx_split_image[k].GetWidth()                       #读取验证码图像的宽和高
            h = wx_split_image[k].GetHeight()
            dis_split_image.append(wx_split_image[k].Scale(w*3,h*3))
            wx.StaticBitmap(self, -1,wx.BitmapFromImage(dis_split_image[k]),pos = (310+k*100,350))
            #plt.figure("IMAGE")       #用matplotlib画出图像 
            #plt.imshow(split_result[k])
            #plt.show() 

    def Pic_iden_event(self,event):
        single_cap = []
        single_cap.append(image_queue.get()) #读入4张单字符图像
        cap_feature = image_predict.featrue_generate(single_cap)
        model = joblib.load(model_path)      #加载识别的模型
        predict_array = model.predict(cap_feature[0])
        predict = ''.join(predict_array)
        big_title = wx.Font(25,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD) #加粗文字格式  25
        dis_result = wx.StaticText(self, label='识别结果为：' + predict,pos = (340,500))
        dis_result.SetForegroundColour('#33539e')   #86e3ce  16a5a3
        dis_result.SetBackgroundColour('#ec6091')   #fa897b
        dis_result.SetFont(big_title)
        print(predict)

if __name__ == '__main__':
   
    app = wx.App()
    Example(None, title='验证码识别')
    app.MainLoop()