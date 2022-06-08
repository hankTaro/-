#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
import optparse
import numpy as np
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog


# In[2]:


def en_to_bin(char):
    bin_char = bytes(char, 'ascii')
    bin_arr=""
    for x in bin_char:
        bin_arr+="{:08b}".format(x)
    return bin_arr


# In[3]:


def encode(num, bit):
    return int(bin(num)[:-1] + bit, 2)


# In[4]:


#RGBA用
def hide_char_to_img(filename, char):
    temp = Image.open(filename)
    
    #將圖片轉為RGBA格式
    if temp.mode != 'RGBA':
        img = temp.convert("RGBA")
    else:
        img = temp
        
    #加入中止資料
    bin_str=en_to_bin(char)+"1111111111111110"
    
    #將圖片的像素資料載入
    raw_data=img.getdata()
    
    #由於每個像素是由RGBA四個byte組成 所以像素量*4就是可改變的資料量(因為只會改會右側的bit
    if(len(bin_str)>len(raw_data)*4):
        return "image's pixal not enough"
    
    encrypted_data=[]
    counter=0
    check=True #檢查要加密的值是否結束 
    for pix in raw_data:
        if check==True:
            encrypted_pix=[]
            for RGBA in pix:
                if counter<len(bin_str):
                    encrypted_pix.append(encode(RGBA, bin_str[counter]))
                    counter+=1
                else:
                    encrypted_pix.append(RGBA)
                    check=False
            encrypted_data.append(tuple(encrypted_pix))
        else:
            break
            
    img.putdata(encrypted_data)
    img.save("secret_text.png")
    return "done"


# In[5]:


#RGB用
def hide_char_to_img2(filename, char):
    temp = Image.open(filename)
    
    #將圖片轉為RGB格式
    if temp.mode != 'RGB':
        img = temp.convert("RGB")
    else:
        img = temp
        
    #將文字轉成二進位 並加入中止資料
    bin_str=en_to_bin(char)+"1111111111111110"
    
    #將圖片的像素資料載入
    raw_data=img.getdata()
    
    #由於每個像素是由RGB三個byte組成 所以像素量*3就是可改變的資料量(因為只會改會右側的bit
    if(len(bin_str)>len(raw_data)*3):
        return "image's pixal not enough"
    
    encrypted_data=[]
    counter=0
    check=True #檢查要加密的值是否結束 
    for pix in raw_data:
        if check==True:
            encrypted_pix=[]
            for RGB in pix:
                if counter<len(bin_str):
                    encrypted_pix.append(encode(RGB, bin_str[counter]))
                    counter+=1
                else:
                    encrypted_pix.append(RGB)
                    check=False
            encrypted_data.append(tuple(encrypted_pix))
        else:
            break
            
    img.putdata(encrypted_data)
    img.save("secret_text.png")
    return "done"


# In[6]:


def bin_to_en(bin_char):
    counter=0
    char_arr=""
    temp=""

    for x in bin_char:
        temp+=x
        if counter!=7:
            counter+=1
        else:
            char_arr+=chr(int(temp, 2))
            counter=0
            temp=""
            
    return char_arr


# In[7]:


def img_to_bin(filename):
    temp = Image.open(filename)
    
        
    #將圖片轉為RGB格式
    if temp.mode != 'RGB':
        img = temp.convert("RGB")
    else:
        img = temp
    
    #取得圖片的長寬pix
    w=img.width
    h=img.height

    #將前面24bit作為長寬資訊保存 最大只能接受4096*4096 pix 的圖檔
    bin_str = ""+"{:012b}{:012b}".format(w,h)

    raw_data = img.getdata()
    for pix in raw_data:
        for RGB in pix:
            bin_str+="{:08b}".format(RGB)
    return bin_str


# In[8]:


def hide_img_to_img(filename,pic):
    temp = Image.open(filename)
    
    #將圖片轉為RGBA格式
    if temp.mode != 'RGBA':
        img = temp.convert("RGBA")
    else:
        img = temp

    
    #將文字轉成二進位 並加入中止資料 紅綠藍黑白
    end_point="{:08b}{:08b}{:08b}".format(255,0,0)+"{:08b}{:08b}{:08b}".format(0,255,0)    +"{:08b}{:08b}{:08b}".format(0,0,255)+"{:08b}{:08b}{:08b}".format(0,0,0)+"{:08b}{:08b}{:08b}".format(255,255,255)
    
    bin_str=img_to_bin(pic)+end_point

    #將圖片的像素資料載入
    raw_data=img.getdata()
    
    #由於每個像素是由RGBA四個byte組成 所以像素量*4就是可改變的資料量(因為只會改會右側的bit
    if(len(bin_str)>len(raw_data)*4):
        return "image's pixal not enough"
    
    encrypted_data=[]
    counter=0
    check=True #檢查要加密的值是否結束 
    for pix in raw_data:
        if check==True:
            encrypted_pix=[]
            for RGBA in pix:
                if counter<len(bin_str):
                    encrypted_pix.append(encode(RGBA, bin_str[counter]))
                    counter+=1
                else:
                    encrypted_pix.append(RGBA)
                    check=False
            encrypted_data.append(tuple(encrypted_pix))
        else:
            break
            
    img.putdata(encrypted_data)
    img.save("secret_img.png")
    return "done"


# In[9]:


def show_word(filename):
    img = Image.open(filename)
    bin_str = ""

    if img.mode == 'RGBA' or img.mode == 'RGB':
        raw_data = img.getdata()
        for pix in raw_data:
            for RGBA in pix:
                bin_str += bin(RGBA)[-1]
                if bin_str[-16:] == "1111111111111110":
                    print("done")
                    return bin_to_en(bin_str[:-16])
        return "未搜索到中止碼，此圖片可能未經隱寫" 
    return "錯誤的檔案格式，無法解碼"


# In[10]:


def show_img(filename):
    img = Image.open(filename)
    bin_str = ""
    end_point="{:08b}{:08b}{:08b}".format(255,0,0)+"{:08b}{:08b}{:08b}".format(0,255,0)    +"{:08b}{:08b}{:08b}".format(0,0,255)+"{:08b}{:08b}{:08b}".format(0,0,0)+"{:08b}{:08b}{:08b}".format(255,255,255)
    

    if img.mode == 'RGBA' or img.mode == 'RGB':
        raw_data = img.getdata()
        
        counter=0
        for pix in raw_data:
            if counter==24:
                break
            for RGBA in pix:
                if counter==24:
                    break
                else:
                    counter+=1
                    bin_str += bin(RGBA)[-1]
                
        #設定輸出的長寬 也就是存在前24個pix中的資訊        
        hide_img=Image.new(mode = "RGB",size=(int(bin_str[:12],2),int(bin_str[12:24],2)))
        
        hide_data=[]
        hide_pix=[]
        hide_RGB=""
        pix_counter=0
        RGB_counter=0
        counter=0
        for pix in raw_data:
            for RGBA in pix:
                if counter==24:
                    bin_str += bin(RGBA)[-1]
                    hide_RGB += bin(RGBA)[-1]
                    RGB_counter+=1
                    if RGB_counter==8:
                        RGB_counter=0
                        hide_pix.append(int(hide_RGB,2)) 
                        pix_counter+=1
                        hide_RGB=""

                    if pix_counter==3:
                        pix_counter=0
                        hide_data.append(tuple(hide_pix)) 
                        hide_pix=[]

                    if bin_str[-120:] == end_point:  
                        for a in range(5):
                            hide_data.pop()
                        hide_img.putdata(hide_data)
                        hide_img.save("hide_img.png")
                        hide_img.show()
                        return "done"
                else:
                    counter+=1
            
        return "未搜索到中止碼，此圖片可能未經隱寫" 
    return "錯誤的檔案格式，無法解碼"


# In[11]:


def start():
    print("請先將欲作為基底的圖片命名為 base.jpg 放入同個資料夾內")
    print("並將欲隱藏的圖片命名為 hide.jpg 放入同個資料夾內")
    func_mod=input("請問要隱寫還是解出隱藏訊息\n隱寫輸入:1  解出隱藏訊息輸入:2\n")
    if func_mod=='1':
        func_mod=input("請問要隱寫文字還是圖片\n文字輸入:1  圖片輸入:2\n")
        if func_mod=='1':
            text = input("輸入要隱藏的訊息(必須是英文): \n")
            color_mod = input("輸入要使用何種編碼方式 (RGB輸入:1 RGBA輸入:2): \n")
            if color_mod=='1':
                return hide_char_to_img2('base.jpg', text)
            if color_mod=='2':
                return hide_char_to_img('base.jpg', text)
        elif func_mod=='2':
            return hide_img_to_img('base.jpg', 'hide.jpg')
        else:
            return "無法識別的指令"
            
    elif func_mod=='2':
        func_mod=input("請問是要解出隱寫文字還是圖片\n文字輸入:1  圖片輸入:2 \n")
        if func_mod=='1':
            return "隱藏的文字是:"+show_word('secret_text.png')
        elif func_mod=='2':
            return "隱藏的圖片是:"+show_img('secret_img.png')
    else:
        return "無法識別的指令"


# In[12]:


# # 請先將欲作為基底的圖片命名為 base.jpg 放入同個資料夾內
# # 並將欲隱藏的圖片命名為 hide.jpg 放入同個資料夾內
# ans=start()
# print(ans)


# In[13]:


show_word('secret_text.png')


# In[14]:


def enter():
    if text.get()=='':
        tkinter.messagebox.showinfo(title = '系統訊息',message = "請先輸入要隱藏的文字") 
        return 0
    msg="選擇載體圖片"
    file_path=open_file(msg)
    msg=hide_char_to_img(file_path, text.get())
    tkinter.messagebox.showinfo(title = '系統訊息',message = msg) 
def enter2():
    if text.get()=='':
        tkinter.messagebox.showinfo(title = '系統訊息',message = "請先輸入要隱藏的文字") 
        return 0
    msg="選擇載體圖片"
    file_path=open_file(msg)
    msg=hide_char_to_img2(file_path, text.get())
    tkinter.messagebox.showinfo(title = '系統訊息',message = msg) 
def enter3():
    file_path=open_file_seek()
    msg=show_word(file_path)
    tkinter.messagebox.showinfo(title = '系統訊息',message = '隱藏的文字是:'+msg) 
def enter4():
    file_path=open_file_seek()
    msg=show_img(file_path)
    tkinter.messagebox.showinfo(title = '系統訊息',message = msg) 
def enter5():
    msg="選擇載體圖片"
    file_path=open_file(msg)
    msg="選擇要隱寫圖片"
    b=open_file(msg)
    msg=hide_img_to_img(file_path, b)
    tkinter.messagebox.showinfo(title = '系統訊息',message = msg) 


# In[15]:


def open_file(msg):
    window = tk.Tk()
    window.withdraw()
    file_path = filedialog.askopenfilename(parent=window, title=msg, filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return file_path

def open_file_seek():
    window = tk.Tk()
    window.withdraw()
    file_path = filedialog.askopenfilename(parent=window, title="選擇要找出隱藏資料的圖片", filetypes = (("png files","*.png"),("all files","*.*")))
    return file_path


# In[16]:


# 建立主視窗 Frame
window = tk.Tk()

# 設定視窗標題
window.title('圖片隱寫')

# 設定視窗大小為 300x100，視窗（左上角）在螢幕上的座標位置為 (250, 150)
window.geometry("800x800")

# 標示文字
label = tk.Label(window, text = '輸入要隱寫的文字(只能是英文)')
label.pack()

var = tk.StringVar()
text = tk.Entry(window,width = 20,textvariable=var) # 輸入欄位的寬度
text.pack()

# 建立按鈕
button1 = tk.Button(window,text = '隱寫文字 by RGBA',command = enter)  #hide_char_to_img('base.jpg', text.get())
button2 = tk.Button(window,text = '隱寫文字 by RGB',command = enter2)
button3 = tk.Button(window,text = '隱寫圖片',command = enter5)
button4 = tk.Button(window,text = '解出隱藏訊息',command = enter3)
button5 = tk.Button(window,text = '解出隱藏圖片',command = enter4)








# 以預設方式排版按鈕
# button3.pack()
button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()


# 執行主程式
window.mainloop()


# In[ ]:




