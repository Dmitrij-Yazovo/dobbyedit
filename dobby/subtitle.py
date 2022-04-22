import cv2
import sys
from dobby.clova import ClovaSpeechClient
import numpy as np
import moviepy.editor as mp
import os
from PIL import ImageFont,Image,ImageDraw

def subtitle_fps(txt_pth, video_pth):
    res = ClovaSpeechClient().req_upload(file='C:\django\dobbyedit\dobbyedit\dobby\static\media.mp4', completion='sync')
    dt = res.json()
    cap1 = cv2.VideoCapture(video_pth)
    fps2 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = round(fps2) + 2
    test = dt['segments']
    cnt = 0
    start_point = 0
    # 파일 저장되는 경로 -> 변경 해줘야함
    with open(txt_pth, 'a') as f:
        for i in range(len(test)):
            if i == 0 and (test[i]['start']//1000) != 0:
                cnt = (test[i]['start']//1000)* fps2
                for j in range(cnt):
                       f.write(str(" "))
                       f.write("\n")
            cnt = ( (test[i]['end']//1000) - (test[i]['start']//1000) )* fps2
            for j in range(cnt):
                f.write(str(test[i]['text']))
                f.write("\n")
                start_point += 1



def subtitle_generator(txt_pth,video_pth,fontnum,font_col_num,font_bg_num):
# def subtitle_generator(txt_pth,video_pth):
  cap1 = cv2.VideoCapture(video_pth)
  file = open(txt_pth, "r")

  w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
  h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

  fps2 = cap1.get(cv2.CAP_PROP_FPS)
  fps2 = round(fps2)
  fourcc = cv2.VideoWriter_fourcc(*"mp4v")
  delay2 = round(1000/fps2)

  out = cv2.VideoWriter("C:/django/dobbyedit/dobbyedit/dobby/static/test.mp4",fourcc,fps2,(w,h)) #출력 동영상(음성x) 저장될 경로



  fps1 = cap1.get(cv2.CAP_PROP_FPS)
  delay2 = round(1000/fps1)


  if not cap1.isOpened() :
      print("video open failed")
      sys.exit()
  
  # django-to-subtitle.py
  fontnum = fontnum
  font_col_num = font_col_num
  font_bg_num = font_bg_num

  if fontnum == 1:
      fontpath = 'C:/django/dobbyedit/dobbyedit/dobby/static/fonts/Caveat-VariableFont_wght.ttf'
  elif fontnum == 2:
      fontpath = 'C:\django\dobbyedit\dobbyedit\dobby\static/fonts\IndieFlower-Regular.ttf'
  elif fontnum == 3:
      fontpath = 'C:\django\dobbyedit\dobbyedit\dobby\static/fonts\Montserrat-Italic-VariableFont_wght.ttf'
  
#   폰트컬러 흰,검,빨 순
  if font_col_num == 1:
      fontcolor = (255,255,255)
  elif font_col_num == 2:
      fontcolor = (0,0,0)
  elif font_col_num == 3:
      fontcolor = (255,0,0)
  
#   배경색 검,회,흰 순
  if font_bg_num == 1:
      bgcolor = (0,0,0,50)
  elif font_bg_num == 2:
      bgcolor = (128,128,128,50)
  elif font_bg_num == 3:
      bgcolor = (255,255,255,50)
  #
  while True:
      ret,frame = cap1.read()
      if not ret: 
          break
      org=(0,620)
    #   font=cv2.FONT_HERSHEY_SIMPLEX #font 설정
    #   fontpath = font
    #   print(type(fontpath))
      font = ImageFont.truetype(fontpath,32)
      text = file.readline()
      text_size =font.getsize(text)  
      if text_size[0] > w:
          text = text.split()
          n = len(text) //2
          text = text[:n] + ['\n'] + text[n:]
          text = ' '.join(text)

      
      y0, dy = 620, text_size[1]

    #   for i, line in enumerate(text.split('\n')):
    #       y = y0 + i*dy
    #     #  cv2.rectangle(frame,(0,y),(org[0]+size[0],y),(0,0,255),-1) # 글자 배경 지정 ( 색상 : (255,0,0))
    #       #cv2.rectangle(frame,(0,y),(org[0]+size[0],y-size[1]),(0,0,255),-1) # 글자 배경 지정 ( 색상 : (255,0,0))

    #       img = Image.fromarray(frame)
    #       draw = ImageDraw.Draw(img, 'RGBA')
    #       draw.rectangle((0,y,org[0]+text_size[0],y-text_size[1]),fill=(128,128,128,50))
    #       frame = np.array(img)
    #       img = Image.fromarray(frame)
    #       draw2 = ImageDraw.Draw(img)
    #       draw2.text((0, y),line,font = font,fill = (255,255,255,255))
    #       frame = np.array(img)

          
          #cv2.putText(frame, line, (0, y ), font, 1,(255,0,0), 2) # 글자 넣기 ( 색상 : (255,0,0))    
      # 미리보기 cv2.imshow("frame",frame)
      line = text.split('\n')
      img = Image.fromarray(frame)
      draw = ImageDraw.Draw(img, 'RGBA')
      draw.rectangle((0,y0-text_size[1],text_size[0],y0+text_size[1]),fill=bgcolor)
      frame = np.array(img)
      img = Image.fromarray(frame)
      draw2 = ImageDraw.Draw(img)
      draw2.text((0, y0),line[1],font = font,fill = fontcolor)
      frame = np.array(img)
      img = Image.fromarray(frame)
      draw3 = ImageDraw.Draw(img)
      draw3.text((0, y0-text_size[1]),line[0],font = font,fill = fontcolor)
      frame = np.array(img)
      
          
      out.write(frame)

      # if cv2.waitKey(delay2) == 27:
      #    break

def combine_audio(video_pth):
    videoclip = mp.VideoFileClip("C:/django/dobbyedit/dobbyedit/dobby/static/test.mp4") # 자막이 들어간 동영상 위치
    audioclip = mp.AudioFileClip(video_pth) # 원본 동영상 위치

    videoclip = videoclip.set_audio(audioclip)  

    videoclip.write_videofile("C:/django/dobbyedit/dobbyedit/dobby/static/new_test_sub.mp4",codec='libx264',audio_codec='aac')