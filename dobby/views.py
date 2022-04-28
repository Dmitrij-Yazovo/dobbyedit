import datetime
import os
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from config import settings
from config.settings import MEDIA_ROOT
from dobby.fu_filter import combine_audio2, filter_srt, total_filter
from django.core.files.storage import FileSystemStorage
from dobby.subtitle import combine_audio, subtitle_fps, subtitle_generator
from main.models import Member
from .models import File, Inputfile

# Create your views here.
def edit(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    if request.method == "POST":
        upload_file = request.FILES.get('e_file')
        name = upload_file.name 
        request.session['file_name'] = name
        with open(MEDIA_ROOT+'/'+name, 'wb') as file: 
            for chunk in upload_file.chunks():
                file.write(chunk)

    else:
        return render(request, "dobby/edit.html")
    
    # return render(request, "dobby/fun.html", {"upload_file": upload_file})
    return redirect("/dobby/fun/")


def result(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")

    return render(request, 'dobby/result.html')




def fun(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")

    global fontnum
    global font_col_num
    global font_bg_num
    # return render(request,"dobby/fun.html")
    if request.method == "GET":
      
        return render(request,"dobby/fun.html")
        
    elif 'create' in request.POST:
        txt_pth = MEDIA_ROOT + "\\"+ "subtitle.txt"
        video_pth = MEDIA_ROOT + "\\" + request.session['file_name']
    
        font =  request.POST['font']
        if font == "font1":
            fontnum = 1

        elif font == "font2":
            fontnum = 2

        elif font == "font3":
            fontnum = 3

        fontcolor =  request.POST['fontcolor']
        if fontcolor == "font-color1":
            font_col_num = 1

        elif fontcolor == "font-color2":
            font_col_num = 2

        elif fontcolor == "font-color3":
            font_col_num = 3


        font_bg_num = 0
        bgcolor =  request.POST['bgcolor']
        if bgcolor == "bg-color1":
            font_bg_num = 1

        elif bgcolor == "bg-color2":
            font_bg_num = 2

        elif bgcolor == "bg-color3":
            font_bg_num = 3
        
        subtitle_fps(txt_pth,video_pth)
        subtitle_generator(txt_pth,video_pth,fontnum,font_col_num,font_bg_num)
        combine_audio(video_pth, request.session['file_name'])
        
        
        file_path = str(settings.BASE_DIR) + ('/media/%s' % request.session['file_name'])
        rmv1 = str(settings.BASE_DIR) + ('/media/%s' % 'no_voice.mp4')
        rmv2 = str(settings.BASE_DIR) + ('/media/%s' % 'subtitle.txt')
        os.remove(file_path)
        os.remove(rmv1)
        os.remove(rmv2)
        
        now = datetime.datetime.now()
        
        file = File(
            file_name = request.session['file_name'],
            member_id = Member.objects.get(member_id=request.session.get('s_id')),
            file_root = "\\media\\subtitle\\" + request.session['file_name'],
            file_date = now,
        )
        file.save()

    
    elif 'filter' in request.POST:
        txt_pth = MEDIA_ROOT + "\\"+ "result.txt"  # 필터링 음성추출파일 
        video_pth = MEDIA_ROOT + "\\" + request.session['file_name']
 
        
        filter_srt(txt_pth,video_pth)
        total_filter(txt_pth,video_pth)
        
        audio_pth =  MEDIA_ROOT + "\\" + "filter_audio.mp3"
        combine_audio2(audio_pth,video_pth,request.session['file_name'])
        
        now = datetime.datetime.now()
        
        file = File(
            file_name = request.session['file_name'],
            member_id = Member.objects.get(member_id=request.session.get('s_id')),
            file_root = "\\media\\filter\\" + request.session['file_name'],
            file_date = now,
        )
        file.save()

    return render(request, 'dobby/result.html', {'file':file})
                    # # return render(request,"dobby/fun.html")
                    # if request.method == "GET":
                        
                    #     file_root = os.path.join(MEDIA_ROOT+'/')
                    #     ####################################################
                        
                    #     ####################################################
                        
                        
                    #     return render(request, "dobby/fun.html")
                    
                    # elif 'create' in request.POST:
                    #     txt_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\subtitle.txt"
                    #     video_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\media.mp4"
                    #     subtitle_fps(txt_pth,video_pth)
                    #     subtitle_generator(txt_pth,video_pth)
                    #     combine_audio(video_pth)
                    
                    # elif 'filter' in request.POST:
                    #     txt_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/result.txt"
                    #     video_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/media_ssiba.mp4"
                    #     filter_srt(txt_pth,video_pth)
                    #     total_filter(txt_pth,video_pth)
                    #     audio_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/one_final.mp3"
                    #     combine_audio2(audio_pth,video_pth)

                    # return render(request, 'dobby/result.html')

# def fun(request):
    
   
    
#     if request.method == "GET":
#         return render(request, "dobby/fun.html")
    
#     # 로딩페이지 테스트용함수
#     elif 'shorts' in request.POST:
#         time.sleep(10)
        
#         return render(request, "dobby/result.html")

#     elif 'create' in request.POST:
#         txt_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\subtitle.txt"
#         video_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\media.mp4"
        
#         font =  request.POST['font']
#         if font == "font1":
#             fontnum = 1
        
#         elif font == "font2":
#             fontnum = 2
        
#         elif font == "font3":
#             fontnum = 3
        
#         fontcolor =  request.POST['fontcolor']
#         if fontcolor == "font-color1":
#             font_col_num = 1
        
#         elif fontcolor == "font-color2":
#             font_col_num = 2
        
#         elif fontcolor == "font-color3":
#             font_col_num = 3
        
#         font_bg_num = 1

#         bgcolor =  request.POST['bgcolor']
#         if bgcolor == "bg-color1":
#             font_bg_num = 1
        
#         elif bgcolor == "bg-color1":
#             font_bg_num = 2
        
#         elif bgcolor == "bg-color1":
#             font_bg_num = 3

        
        
#         subtitle_fps(txt_pth,video_pth)
#         subtitle_generator(txt_pth,video_pth,fontnum,font_col_num,font_bg_num)
#         # subtitle_generator(txt_pth,video_pth)
#         combine_audio(video_pth)
    
    # elif 'filter' in request.POST:
    #     txt_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/result.txt"
    #     video_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/media_ssiba.mp4"
    #     filter_srt(txt_pth,video_pth)
    #     total_filter(txt_pth,video_pth)
    #     audio_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/one_final.mp3"
    #     combine_audio2(audio_pth,video_pth)

    # return render(request, 'dobby/result.html')

   