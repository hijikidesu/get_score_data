import cv2
import numpy as np
import customtkinter
import tkinter as tk
import os
import get_score_method
import threading
from PIL import Image, ImageTk
import pandas as pd
from tkinter import messagebox

FONT_TYPE = "meiryo"

class App(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        
        #メンバー変数の設定
        self.fonts = (FONT_TYPE,15)
        
        #画像データのパスを保持する変数
        self.bg_img_path = None  # 背景
        self.notes_img_path = None 
        self.bpm_img_path = None 
        
        #フォームのセットアップをする
        self.setup_form()
        
    def setup_form(self):
        #フォームサイズ設定
        #self.geometry("800x500")
        self.title("score_reader")
        
        #レイアウト設定
        self.grid_rowconfigure(1,weight=1) #行方向
        self.grid_columnconfigure(0,weight=1) #列方向
        
        #URL読み込みフレームの設定
        self.get_score_frame = GetScoreFrame(master=self,header_name = "URL読み込み")
        self.get_score_frame.grid(row=0,column=0,padx=20,pady=20,sticky="ew")
        
        
class GetScoreFrame(customtkinter.CTkFrame):
    
    def __init__(self,*args,header_name="GetScoreFrame", **kwargs):
        super().__init__(*args,**kwargs)
        
        #メンバ関数の設定
        self.fonts = (FONT_TYPE,15)
        self.header_name = header_name
        
        #フォームのセットアップをする
        self.setup_form()
        
    def setup_form(self):
        #レイアウト設定
        self.grid_rowconfigure(0,weight=1) #行方向
        self.grid_columnconfigure(0,weight=1) #列方向
        
        #URLを指定するテキストボックス
        self.URL_textbox = customtkinter.CTkEntry(master=self,placeholder_text="URLをここにコピー",width=120,font=self.fonts)
        self.URL_textbox.grid(row=0,column=0,padx=10,pady=(0,10),sticky="ew")
        
        #曲名を指定するテキストボックス
        self.music_name_textbox = customtkinter.CTkEntry(master=self,placeholder_text="曲名を入れてね",width=120,font=self.fonts)
        self.music_name_textbox.grid(row=1,column=0,padx=10,pady=(0,10),sticky="ew")
        
        #実行ボタン
        self.get_score_button = customtkinter.CTkButton(master=self,fg_color="transparent",border_width=2,text_color=("gray10","#DCE4EE"),
                                                     command=lambda:self.get_score_button_callback(self.URL_textbox),text="譜面データ取得",font=self.fonts)
        self.get_score_button.grid(row=1,column=1,padx=10,pady=(0,10))
        
            
            
    def get_score_button_callback(self):
        """
        譜面データ取得ボタンが押されたときのコールバック。
        """
        
        URL_path = self.URL_textbox.get()
        music_name = self.music_name_textbox.get()

        self.master.bg_img_path,self.master.notes_img_path,self.master.bpm_img_path = get_score_method.get_score_image(URL_path,music_name)
        get_score_method.score_reader(music_name,self.master.bg_img_path,self.master.notes_img_path,self.master.bpm_img_path)
        messagebox.showinfo(
        title='完了', # Windowsの場合のみ
        message='譜面データ読み取り完了!'
        )
        

            
            
 
        

if __name__ == "__main__":
    app = App()
    # ウィンドウの表示
    app.mainloop()