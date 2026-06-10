import cv2
import numpy as np
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from time import sleep
import random
import os

#Byで利用するやつ
TAG_NAME = "tag name"
CLASS_NAME = "class name" 

 
#画像をdataファイルに保存
def download_image(image_url,file_name,save_dir):
    # 完全なファイルパスを作成
    file_path = os.path.join(save_dir, file_name)
    response = requests.get(image_url)
    sleep(5)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return file_path

def get_score_image(url,music_name):
    save_dir = "score_image_file" #相対パス
    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(save_dir):
       os.makedirs(save_dir)

    driver = webdriver.Chrome()
    driver.implicitly_wait(10) #暗黙的な待機

    driver.get(url) 
    sleep(5)
    img_tags = driver.find_elements(By.TAG_NAME , 'img') 

    if img_tags:
        bg_img_src = img_tags[5].get_attribute('src')
        sleep(3)
        notes_img_src = img_tags[6].get_attribute('src')
        sleep(3)
        bpm_img_src = img_tags[7].get_attribute('src')
        sleep(3)
        bg_file_path = download_image(bg_img_src , music_name + '_bg.png',save_dir)
        notes_file_path = download_image(notes_img_src , music_name + '_notes_data.png',save_dir)
        bpm_file_path = download_image(bpm_img_src , music_name + '_bpm.png',save_dir)
        print('ok!')
    else:
        print("画像が見つかりませんでした。")

    driver.quit()
    return bg_file_path,notes_file_path,bpm_file_path


WHITE_MIN_COLOR = np.array([0, 0, 60])  # 下限の色 (HSV)
WHITE_MAX_COLOR = np.array([0, 0, 255])  # 上限の色 (HSV)

# BTの色の範囲を定義
BT_MIN_COLOR = np.array([0, 0, 100])  # 下限の色 (HSV)
BT_MAX_COLOR = np.array([180 , 50, 255])  # 上限の色 (HSV)

#赤つまみが被ってるBTの色の範囲を定義
BT_RED_COVERAGE_MIN_COLOR = np.array([150,0,150]) #下限
BT_RED_COVERAGE_MAX_COLOR = np.array([235,177,247]) #上限

#青つまみが被ってるBTの色の範囲を定義
BT_BLUE_COVERAGE_MIN_COLOR = np.array([60,0,90]) #下限
BT_BLUE_COVERAGE_MAX_COLOR = np.array([120,200,247]) #上限

 # FXの色の範囲を定義
FX_MIN_COLOR = np.array([10, 100, 100])  # 下限の色 (HSV)
FX_MAX_COLOR = np.array([30 , 255, 255])  # 上限の色 (HSV)

#赤つまみが被ってるFXの色の範囲を定義
FX_RED_COVERAGE_MIN_COLOR = np.array([168,0,180]) #下限
FX_RED_COVERAGE_MAX_COLOR = np.array([180,171,252]) #上限

#青つまみが被ってるFXの色の範囲を定義
FX_BLUE_COVERAGE_MIN_COLOR = np.array([60,0,50]) #下限
FX_BLUE_COVERAGE_MAX_COLOR = np.array([180,130,205]) #上限

# 赤つまみの色の範囲を定義
RED_TUMAMI_MIN_COLOR = np.array([145, 0, 100])  # 下限の色 (HSV)
RED_TUMAMI_MAX_COLOR = np.array([179 , 255, 255])  # 上限の色 (HSV)

# 青つまみの色の範囲を定義
BLUE_TUMAMI_MIN_COLOR = np.array([60, 0, 80])  # 下限の色 (HSV)
BLUE_TUMAMI_MAX_COLOR = np.array([140 , 255, 255])  # 上限の色 (HSV)

#重なっているつまみの色の範囲を定義
DOUBLE_TUMAMI_MIN_COLOR = np.array([105, 130, 140])  # 下限の色 (HSV)
DOUBLE_TUMAMI_MAX_COLOR = np.array([250, 175, 245])  # 上限の色 (HSV)

# BPMの色の範囲を定義
BPM_MIN_COLOR = np.array([47, 255, 255])  # 下限の色 (HSV)
BPM_MAX_COLOR = np.array([49 , 255, 255])  # 上限の色 (HSV)
    

def barline_checker(img):

    
    #小節線を検出
    img = cv2.inRange(img , WHITE_MIN_COLOR , WHITE_MAX_COLOR)
    
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    #y座標をリスト化する
    y_list=[]
    #print(len(contours)) #小節線の数

    for contour in contours:
        for y_point in contour:
            y_list.append(y_point[0][1])

    y_list = list(set(y_list))#重複取り除き
    y_list.sort(reverse=True)

    return y_list


def beat_checker(bar_interval):

    #?/4拍子
    if bar_interval == 96:
        beat = 2

    elif bar_interval == 120:
        beat = 2.5 #5/8拍子
        
    elif bar_interval == 108 or bar_interval == 144:
        beat = 3

    elif bar_interval == 168:
        beat == 3.5 #7/8拍子

    elif bar_interval == 192:
        beat = 4
        
    elif bar_interval == 180 or bar_interval == 240:
        beat = 5

    elif bar_interval == 216:
        beat = 6

    elif bar_interval == 252:
        beat = 7
        
    return beat


def number_of_sixteenth_notes_checker(beat):
    #1小節中の16分の数
    
    number_of_sixteenth_notes_in_measure = int(beat * 4)
            
    return number_of_sixteenth_notes_in_measure


def number_of_twenty_four_notes_checker(beat):
    #1小節中の24分の数

    number_of_twenty_four_notes_in_measure = int(beat * 6)

    return number_of_twenty_four_notes_in_measure


def number_of_thirty_second_notes_checker(beat):
    #1小節中の32分の数

    number_of_thirty_second_notes_in_measure = int(beat * 8)
     
    return number_of_thirty_second_notes_in_measure


def generate_note_mask(img , min_color1 , max_color1 , min_color2 , max_color2 , min_color3 , max_color3):
    
    mask1 = cv2.inRange(img , min_color1 , max_color1)
    mask2 = cv2.inRange(img , min_color2 , max_color2)
    mask3 = cv2.inRange(img , min_color3 , max_color3)

    combined_mask = cv2.bitwise_or(mask1,mask2)
    combined_mask = cv2.bitwise_or(mask3,combined_mask)

    return combined_mask


def generate_tumami_mask(img , min_color , max_color ):

    mask1 = cv2.inRange(img , min_color , max_color)
    mask2 = cv2.inRange(img , DOUBLE_TUMAMI_MIN_COLOR , DOUBLE_TUMAMI_MAX_COLOR)

    combined_mask = cv2.bitwise_or(mask1,mask2)
    
    return combined_mask


def bt_checker(contours,is_fx): #btの種類を判断
            
    #どのレーンかの判断に使用
    bt_A_left = 34
    bt_A_to_B = 44
    bt_B_to_C = 54
    bt_C_to_D = 64
    bt_D_right = 74

    bt_data=[0,0,0,0] #btのデータ初期化


    
    
    for contour in contours:
        bt_x_count = np.array([0,0,0,0]) #A,B,C,Dの範囲のｘ座標の数を数え、一番多かったやつを格納する
        if 15 < cv2.contourArea(contour) < 17 or 11< cv2.contourArea(contour) < 13:
            x_coords = contour[:, 0, 0]
            y_coords = contour[:, 0, 1]
  
            if np.min(y_coords) != 0 and np.max(y_coords) != 2:
                
                continue
                
            for x_coord in x_coords:            
                if bt_A_left < x_coord < bt_A_to_B:
                    bt_x_count[0] += 1

                elif bt_A_to_B < x_coord < bt_B_to_C:
                    bt_x_count[1] += 1
        
                elif bt_B_to_C < x_coord < bt_C_to_D:
                    bt_x_count[2] += 1
                    
                elif bt_C_to_D < x_coord < bt_D_right:
                    bt_x_count[3] += 1

            if np.argmax(bt_x_count) == 0:
                bt_data[0] = 1

            elif np.argmax(bt_x_count) == 1:
                bt_data[1] = 1

            elif np.argmax(bt_x_count) == 2:
                bt_data[2] = 1

            elif np.argmax(bt_x_count) == 3:
                bt_data[3] = 1
                

        elif  4 < cv2.contourArea(contour) < 70:

            x_coords = contour[:, 0, 0]
            y_coords = contour[:, 0, 1]
            if is_fx == False:
                if np.min(y_coords) != 0 :
                    
                    continue
                
            for x_coord in x_coords:            
                if bt_A_left < x_coord < bt_A_to_B:
                    bt_x_count[0] += 1
 
                elif bt_A_to_B < x_coord < bt_B_to_C:
                    bt_x_count[1] += 1
        
                elif bt_B_to_C < x_coord < bt_C_to_D:
                    bt_x_count[2] += 1
                    
                elif bt_C_to_D < x_coord < bt_D_right:
                    bt_x_count[3] += 1

            if np.argmax(bt_x_count) == 0:
                bt_data[0] = 2

            elif np.argmax(bt_x_count) == 1:
                bt_data[1] = 2

            elif np.argmax(bt_x_count) == 2:
                bt_data[2] = 2

            elif np.argmax(bt_x_count) == 3:
                bt_data[3] = 2
         
    return bt_data
    

def fx_checker(contours): #btの種類を判断
            
    #どのレーンかの判断に使用
    fx_L_left = 34
    fx_L_to_R = 54
    fx_R_right = 74

    fx_data=[0,0]
    
    for contour in contours:
        if 3 < cv2.contourArea(contour) < 5 or 19 < cv2.contourArea(contour) < 21 or 35 < cv2.contourArea(contour) < 37:
            x_coords=contour[:, 0, 0]
            y_coords = contour[:, 0, 1]
            
            if np.min(y_coords) != 0 and np.max(y_coords) != 2:
                
                continue
                
            for x_coord in x_coords:            
                if fx_L_left < x_coord < fx_L_to_R:
                    fx_data[0]=1

                elif fx_L_to_R < x_coord < fx_R_right:
                    fx_data[1]=1

        elif 10 < cv2.contourArea(contour) < 200 or 5.5 < cv2.contourArea(contour) < 6.5:
            x_coords=contour[:, 0, 0]
            y_coords = contour[:, 0, 1]
            
            if np.min(y_coords) != 0 :
                
                continue
                
            for x_coord in x_coords:            
                 if fx_L_left < x_coord < fx_L_to_R:
                    fx_data[0]=2

                 elif fx_L_to_R < x_coord < fx_R_right:
                    fx_data[1]=2
         
    return fx_data
    

def tumami_checker(contours,is_bt,is_fx): #つまみの種類を判断

    tumami_data='-'
    
    for contour in contours:
        if 10 < cv2.contourArea(contour):
            #一番上のy座標の点たちを取得
            top_y = np.min(contour[:, 0, 1])
            points_top_y = contour[contour[:, 0 ,1] == top_y]

            top_x_coords = points_top_y[:, 0 , 0]
            top_right_x = np.max(top_x_coords)
            top_left_x = np.min(top_x_coords)

            #一番下のy座標の点たちを取得
            bottom_y = np.max(contour[:, 0, 1])
            
            #ノーツあったら取る座標の場所変える
            if is_bt ==True or is_fx ==True:
                bottom_y -= 3
                
            points_bottom_y = contour[contour[:, 0 ,1] == bottom_y]

            bottom_x_coords = points_bottom_y[:, 0 , 0]
            bottom_right_x = np.max(bottom_x_coords)
            bottom_left_x = np.min(bottom_x_coords)

            top_right_point = np.array([top_right_x , top_y]) #右上
            top_left_point = np.array([top_left_x , top_y]) #左上
            bottom_right_point = np.array([bottom_right_x , bottom_y]) #右下
            bottom_left_point = np.array([bottom_left_x , bottom_y]) #左下
            
            #対角線の長さの計算
            right_length = np.linalg.norm(top_right_point - bottom_left_point)
            left_length = np.linalg.norm(top_left_point - bottom_right_point)

            if right_length > left_length:
                tumami_data = 'R'
            elif left_length > right_length:
                tumami_data = 'L'
            
    return tumami_data
    

def bt_reader(img,is_fx): #btを画像から読み取り
 
    mask = generate_note_mask(img,BT_MIN_COLOR,BT_MAX_COLOR,BT_RED_COVERAGE_MIN_COLOR,BT_RED_COVERAGE_MAX_COLOR,BT_BLUE_COVERAGE_MIN_COLOR,BT_BLUE_COVERAGE_MAX_COLOR)
    
    red_fx_mask = cv2.inRange(img , FX_RED_COVERAGE_MIN_COLOR , FX_RED_COVERAGE_MAX_COLOR)
    blue_fx_mask = cv2.inRange(img , FX_BLUE_COVERAGE_MIN_COLOR , FX_BLUE_COVERAGE_MAX_COLOR)
    double_tumami_mask = cv2.inRange(img , DOUBLE_TUMAMI_MIN_COLOR , DOUBLE_TUMAMI_MAX_COLOR)
    red_combined_mask = cv2.bitwise_and(mask,red_fx_mask)
    blue_combined_mask = cv2.bitwise_and(mask,blue_fx_mask)
    double_tumami_combined_mask = cv2.bitwise_and(mask,double_tumami_mask)
    red_inverse_mask = cv2.bitwise_not(red_combined_mask)
    blue_inverse_mask = cv2.bitwise_not(blue_combined_mask)
    double_tumami_inverse_mask = cv2.bitwise_not(double_tumami_combined_mask)
    
    mask = cv2.bitwise_and(mask,red_inverse_mask)
    mask = cv2.bitwise_and(mask,blue_inverse_mask)
    mask = cv2.bitwise_and(mask,double_tumami_inverse_mask)
    
    # Y座標を反転
    mask = cv2.flip(mask, 0)  # 縦方向に反転
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bt_data = bt_checker(contours,is_fx)
    
    if any(value == 1 for value in bt_data):
        is_bt = True
    else:
        is_bt = False
    
    return bt_data , is_bt,contours
    

def fx_reader(img):

    mask = generate_note_mask(img,FX_MIN_COLOR,FX_MAX_COLOR,FX_RED_COVERAGE_MIN_COLOR,FX_RED_COVERAGE_MAX_COLOR,FX_BLUE_COVERAGE_MIN_COLOR,FX_BLUE_COVERAGE_MAX_COLOR)
    
    # Y座標を反転
    mask = cv2.flip(mask, 0)  # 縦方向に反転
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fx_data = fx_checker(contours)

    if any(value == 1 for value in fx_data):
        is_fx = True
    else:
        is_fx = False
        
    return fx_data, is_fx


def red_tumami_reader(img,is_bt,is_fx):

    mask = generate_tumami_mask(img,RED_TUMAMI_MIN_COLOR,RED_TUMAMI_MAX_COLOR)
    blue_tumami_mask =  cv2.inRange(img,BLUE_TUMAMI_MIN_COLOR,BLUE_TUMAMI_MAX_COLOR)
    blue_inverse_mask =  cv2.bitwise_not(blue_tumami_mask)
    mask = cv2.bitwise_and(mask,blue_inverse_mask)
    
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    red_tumami_data = tumami_checker(contours,is_bt,is_fx)
    
    return red_tumami_data


def blue_tumami_reader(img,is_bt,is_fx):
    
    mask = generate_tumami_mask(img,BLUE_TUMAMI_MIN_COLOR,BLUE_TUMAMI_MAX_COLOR)
    
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    blue_tumami_data=tumami_checker(contours,is_bt,is_fx)
    
    return blue_tumami_data


def correct_long(notes_list): #ロングなのに単押しノーツが紛れている場合の対応をする関数
    former = '0'
    for note in range(len(notes_list)):
        if notes_list[note] == 0:
            former = '0'
        if notes_list[note] == 1:
            if former == '2':
                for next in range(note+1,len(notes_list)):
                    if notes_list[next] == 0 or notes_list[next] == 1:
                        break
                    if notes_list[next] == 2:
                        notes_list[note] = 2
                        break   
                    else: 
                        continue
            former = '1'  
        if notes_list[note] == 2:
            former = '2'  



def bpm_change_reader(img):
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#色変換
    _, binary_image = cv2.threshold(img_gray, 160, 255, cv2.THRESH_BINARY)

    img_pil = Image.fromarray(binary_image)  

    tool = pyocr.get_available_tools()[0]  # 使用するOCRツールを取得
    txt = tool.image_to_string(
      img_pil,
      lang="eng",
      builder=pyocr.builders.TextBuilder(tesseract_layout=6)
      )
    return txt


def bpm_change_checker(img,bpm):
    mask = cv2.inRange(img , BPM_MIN_COLOR , BPM_MAX_COLOR)
    
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 1:
            x_coords = contour[:, 0, 0]
            if np.max(x_coords) <16:
                img = img[:,0:13]
            bpm = bpm_change_reader(img)
            break

    try:
        int_bpm = int(bpm)
    except Exception as e:
        print('bpmがうまく読み込めませんでした')
    else:
        return int_bpm

def score_reader(music_name,back_ground_img_file_path,notes_img_file_path,bpm_img_file_path):
    now_time = 0

    bpm = 0 

    img = cv2.imread(notes_img_file_path)
    back_ground_img = cv2.imread(back_ground_img_file_path)
    bpm_img = cv2.imread(bpm_img_file_path)

    time_list = []
    bpm_list = []

    bt_a_list = []
    bt_b_list = []
    bt_c_list = []
    bt_d_list = []

    fx_l_list = []
    fx_r_list = []

    tumami_l_list = []
    tumami_r_list = []

    all_notes_data = pd.DataFrame() #特徴量のデータフレーム

    #img=notes_img

    (h, w) = img.shape[:2] # 画像の高さと幅を取得

    LANE_NUMBER = int(w / 110)
    LANE_WIDE = 110 #レーンの幅
    LANE_START = 5 #初期位置（横）

    back_ground_img = cv2.cvtColor(back_ground_img, cv2.COLOR_BGR2HSV) 
    bpm_img = cv2.cvtColor(bpm_img, cv2.COLOR_BGR2HSV) 
    for w in range(LANE_NUMBER):
        #レーンごとに区切る
        left = int(LANE_WIDE*w+LANE_START)
        right = int(LANE_WIDE*(w+1)+LANE_START)
        vertical_img = img[:,left:right]
        vertical_back_ground_img = back_ground_img[:,left:right]
        vertical_bpm_img = bpm_img[:,left:right]
    
        #小節線の座標を取得
        barline_y_list = barline_checker(vertical_back_ground_img)
    
        for i in range(len(barline_y_list)-1):
            measure_notes_data=[]
            measure_top = barline_y_list[i+1]
            measure_bottom = barline_y_list[i]

            measure_img= vertical_img[measure_top:measure_bottom] #1小節の画像
            measure_bpm_img = vertical_bpm_img[measure_top+180:measure_bottom,75:95]
            bpm = bpm_change_checker(measure_bpm_img,bpm)
            four_seconds = 60/bpm #4分音符がなる間隔
            ninety_sixth_seconds = four_seconds/24 #96分音符がなる間隔
        
            (h, w) = measure_img.shape[:2] # 画像の高さと幅を取得

            beat = beat_checker(h) #この小節の拍子を取得

            #16分
            number_of_sixteenth_notes = number_of_sixteenth_notes_checker(beat)
            sixteenth_cut_interval = h / number_of_sixteenth_notes
            sixteenth_cut_number = 0 #初期化
        
            #24分
            number_of_twenty_four_notes = number_of_twenty_four_notes_checker(beat)
            twenty_four_cut_interval = h / number_of_twenty_four_notes
            twenty_four_cut_number = 0 #初期化

            #32分
            number_of_thirty_second_notes = number_of_thirty_second_notes_checker(beat)
            thirty_second_cut_interval = h / number_of_thirty_second_notes
            thirty_second_cut_number = 0 #初期化

            cut_number = 24 * beat #1小節を区切る数
        
            for t in range(cut_number):
                if t % 3 == 0 or t == 0 : #32分
                
                    cut_top = int(thirty_second_cut_interval*(number_of_thirty_second_notes-(thirty_second_cut_number+1)))
                    cut_bottom = int(thirty_second_cut_interval*(number_of_thirty_second_notes-thirty_second_cut_number))
                    thirty_second_cut_number += 1 #インクリメントしてごめん
                
                if t % 4 == 0 or t == 0 : #24分
                
                    cut_top = int(twenty_four_cut_interval*(number_of_twenty_four_notes-(twenty_four_cut_number+1)))
                    cut_bottom = int(twenty_four_cut_interval*(number_of_twenty_four_notes-twenty_four_cut_number))
                    twenty_four_cut_number += 1 #インクリメントしてごめん

                if t % 6 == 0 or t == 0 : #16分
                
                    cut_top = int(sixteenth_cut_interval*(number_of_sixteenth_notes-(sixteenth_cut_number+1)))
                    cut_bottom = int(sixteenth_cut_interval*(number_of_sixteenth_notes-sixteenth_cut_number))   
                    sixteenth_cut_number += 1 #インクリメントしてごめん

                if t % 3 != 0 and t % 6 != 0 and t % 4 != 0 and t != 0:
                    time_list.append(now_time)
                    bpm_list.append(bpm)
                    bt_a_list.append('-')
                    bt_b_list.append('-')
                    bt_c_list.append('-')
                    bt_d_list.append('-')
    
                    fx_l_list.append('-')
                    fx_r_list.append('-')
                
                    tumami_l_list.append(':')
                    tumami_r_list.append(':')
                    now_time += ninety_sixth_seconds

                    continue

                cut_img = measure_img[cut_top:cut_bottom]
       
                cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2HSV)    
                fx_data , is_fx = fx_reader(cut_img)
                bt_data , is_bt ,contours= bt_reader(cut_img,is_fx)
                red_tumami_data= red_tumami_reader(cut_img,is_bt,is_fx)
                blue_tumami_data = blue_tumami_reader(cut_img,is_bt,is_fx)

                time_list.append(now_time)
                bpm_list.append(bpm)
            
                bt_a_list.append(bt_data[0])
                bt_b_list.append(bt_data[1])
                bt_c_list.append(bt_data[2])
                bt_d_list.append(bt_data[3])

                fx_l_list.append(fx_data[0])
                fx_r_list.append(fx_data[1])
            
                tumami_l_list.append(blue_tumami_data)
                tumami_r_list.append(red_tumami_data)
                now_time += ninety_sixth_seconds

    correct_long(bt_a_list)
    correct_long(bt_b_list)
    correct_long(bt_c_list)
    correct_long(bt_d_list)
    correct_long(fx_l_list)
    correct_long(fx_r_list)

    all_notes_data['time'] = time_list
    all_notes_data['bpm'] = bpm_list

    all_notes_data['bt_a'] = bt_a_list
    all_notes_data['bt_b'] = bt_b_list
    all_notes_data['bt_c'] = bt_c_list
    all_notes_data['bt_d'] = bt_d_list

    all_notes_data['fx_l'] = fx_l_list
    all_notes_data['fx_r'] = fx_r_list

    all_notes_data['tumami_l'] = tumami_l_list
    all_notes_data['tumami_r'] = tumami_r_list
        
    all_notes_data.to_csv(music_name + '_score_data.csv')
