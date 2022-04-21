from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from dobby.fu_filter import combine_audio2, filter_srt, total_filter

from dobby.subtitle import combine_audio, subtitle_fps, subtitle_generator

# Create your views here.
def edit(request):
    
    return render(request,"dobby/edit.html")

def loading(request):
    
    return render(request,"dobby/loading.html")


def result(request):

    return render(request,"dobby/result.html")

def fun(request):
    
    # return render(request,"dobby/fun.html")
    if request.method == "GET":
        return render(request, "dobby/fun.html")
    
    elif 'create' in request.POST:
        txt_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\subtitle.txt"
        video_pth = "C:\django\dobbyedit\dobbyedit\dobby\static\media.mp4"
        subtitle_fps(txt_pth,video_pth)
        subtitle_generator(txt_pth,video_pth)
        combine_audio(video_pth)
    
    elif 'filter' in request.POST:
        txt_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/result.txt"
        video_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/media_ssiba.mp4"
        filter_srt(txt_pth,video_pth)
        total_filter(txt_pth,video_pth)
        audio_pth = "C:/django/dobbyedit/dobbyedit/dobby/static/one_final.mp3"
        combine_audio2(audio_pth,video_pth)

    return render(request, 'dobby/result.html')

# def create_sub(reqeust):
#     if 'create' in reqeust.POST:
#         print(12312312312312)
#         txt_pth = "/static/subtitle.txt"
#         video_pth = "/static/media.mp4"
#         subtitle_fps(txt_pth,video_pth)
#         subtitle_generator(txt_pth,video_pth)
        
#     return redirect("/dobby/result/")
   