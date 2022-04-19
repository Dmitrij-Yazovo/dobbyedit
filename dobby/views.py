from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
def edit(request):
    
    return render(request,"dobby/edit.html")

def loading(request):
    
    return render(request,"dobby/loading.html")


def result(request):
    
    return render(request,"dobby/dobbyResult.html")
