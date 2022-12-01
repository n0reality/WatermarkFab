#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Yen Peishan
v3:
1.新增按鈕介面
2.修正字與圖重複問題
3.修正字太小問題
"""

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import tkinter.ttk as ttk
import tkinter as tk
import time
class GUI:
    def PrintTutorial(self):
        print(u'---------------------------------------------------------------------')
        print(u'@@@@@@@@@@@@@@批量圖片加浮水印並存檔程式使用說明@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(u'')
        print(u'1. 此程式會自動批量選取當下"未編輯"資料夾內的圖片，存新圖至"已編輯"資料夾，同時刪')
        print(u'"未編輯"資料夾內的原圖。')
        print(u'2. 程式需與"未編輯"、"已編輯"、"需要的中文字型.ttf"放一起再執行。')
        print(u'')
        print(u'3. 數入頻率數字太大造成執行時間長屬正常現象。')
        print(u'')
        print(u'4. 每個資料夾配一計數器：同一天流水號持續增加，隔天則流水號歸零。')
        print(u'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(u'---------------------------------------------------------------------')

    
    def SelectRepeatRun(self):
        FreqNo=self.cbb.get()
        #Transfer selected cbbtext(str) to FreqNo(int)
        #預設值
        if FreqNo==self.cbbtext[0]:
            FreqNo=1
        elif FreqNo==self.cbbtext[1]:
            FreqNo=10
        elif FreqNo==self.cbbtext[2]:
            FreqNo=30
        #使用者自定義
        else:
            try:
                FreqNo=int(FreqNo)
            except:
                FreqNo=0#使用者輸出錯誤
                #print(u'[333]輸入錯誤！應輸入一數字')  
        #print(FreqNo)
        #重複十次
        if FreqNo==1:
            self.CreateNewRemoveOld()
        else:
            for i in range(10):
                self.CreateNewRemoveOld()
                time.sleep(FreqNo*60)
    def CreateNewRemoveOld(self):
        TODAY=datetime.now().date().strftime('%Y/%m/%d')
        sourcefolder=os.listdir(u'./未編輯/')
        for folder in sourcefolder:
            try:
                pics=os.listdir(u'./未編輯/'+folder)
                try:
                    cnttxt=open(u'./未編輯/'+folder+'/計數器.txt','r')
                    cnt_cnt=cnttxt.readline()
                    cnt_date=cnttxt.readline()
                    #print('TODAY-+-+-+-)',TODAY,'(+-+-+-+')
                    #print('cnt_date-+-+-+-)',cnt_date,'(+-+-+-+')
                    if cnt_date<TODAY:#若同天流水號持續增加,若隔天流水號歸零
                        cnt_cnt=0
                        print(u'======日期增,流水號歸零=======')
                    cnttxt.close()
                except:
                    cnt_cnt,cnt_date=0,TODAY
                cnt_cnt=int(cnt_cnt)
                for pic in pics:
                    try:
                        #用黑底加寬
                        img = Image.open(u'未編輯/'+folder+'/'+pic).convert('RGBA')
                        #img.thumbnail(img.size, Image.ANTIALIAS)
                        h,w=img.size
                        h_,w_=int(h*0.2),int(w*0.2)
                        h,w=int(h*1.2),int(w*1.2)
                        textsize=int(min(h,w)/10)
                        newimg = Image.new(mode='RGBA',size=(h,w),color=(255,255,255,255))#白底
                        newimg.paste(img, (h_,w_))
                        #newimg.save(u'./已編輯/'+folder+'/哈哈哈測試中.png',format='PNG')
                        
                        #加字於左上角
                        cnt_cnt+=1#確認前沒except才加一
                        draw = ImageDraw.Draw(newimg)
                        text=folder+'_'+str(cnt_cnt)
                        font = ImageFont.truetype(u"需要的中文字型.ttf", textsize)
                        draw.text((0, 0),text,(0,0,0),font)#黑字顏色
                        #新檔名為舊檔名＋新檔名, '.tif','.jpg','.png'是四位,少數如'.jpeg'才五位
                        if '.jpeg' in pic:
                            fname=pic[:-5]
                        else:
                            fname=pic[:-4]
                        newimg.save(u'./已編輯/'+folder+'/'+fname+'_'+folder+'_'+str(cnt_cnt)+'.png',format='PNG')
                        
                        os.remove(u'未編輯/'+folder+'/'+pic)#編輯後(加浮水印)再刪原圖
                    except:
                        #print('[888]Not picture format: ',u'未編輯/'+folder+'/'+pic)
                        ('')#[foolproof]計數器.txt for MacOS 此檔非圖片
                
                cnttxt=open(u'./未編輯/'+folder+u'/計數器.txt','w+')
                cnttxt.write(str(cnt_cnt))
                cnttxt.write('\n')
                cnttxt.write(str(TODAY))
                cnttxt.close()
                
                    
            except:
                #print('[777]Abnormal folder: ',folder)
                ('')#[foolproof].DS_Store for MacOS 此資料夾非正常資料夾
    def __init__( self,root ):
        self.PrintTutorial()
        self.frame = tk.Frame(root)
        self.frame.grid(row=0)
        self.lbl1=tk.Label(text=u'選擇執行頻率，也可輸入一數字n，n分鐘執行一次。\n註:\n1.等n分鐘同時電腦可以照常執行別的程式/軟體\n2.真正執行時間會隨著您電腦開的其他程式所占資源多寡略大於n分鐘')
        self.lbl1.grid(row=1,column=0)
        self.cbbtext=[u'只執行一次',u'每十分鐘執行一次，執行十次',u'每三十分鐘執行一次，執行十次']
        self.cbb=ttk.Combobox(self.frame,values=self.cbbtext)
        self.cbb.grid(row=2,column=0)
        self.btnSelectRepeatRun=tk.Button(self.frame, text=u'執行',command=self.SelectRepeatRun,bg='red',fg='black')
        self.btnSelectRepeatRun.grid(row=3,column=0)
        

root = tk.Tk()
root.title(u'批量圖片加浮水印並存檔程式v3')
root.geometry('300x300')
gui = GUI(root)
root.mainloop()
