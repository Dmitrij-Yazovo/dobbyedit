import datetime
from django.shortcuts import redirect, render
from .models import Post, Member, Comment, Postfile

# Create your views here.
def postlist(request):
    post_list = Post.objects.all()
    
    return render(
        request,
        'board/postlist.html',
        {'post_list': post_list}
    )
    

def post(request, post_no):
    if request.method == 'GET':
        post = Post.objects.get(post_no=post_no)
        comments = Comment.objects.filter(post_no=post_no)
        postfile = Postfile.objects.get(post_no=post_no)
        context = {
            'post':post,
            'comments':comments,
            'postfile':postfile,
        }
        
        return render(request, 'board/post.html', context)
    
    
    # post메서드(댓글등록,삭제)
    else:
        comment = Comment()
        comment.post = post_no
        comment.body = request.POST['body']
        comment.date = datetime.now()
        comment.save()
        return render(request, 'board/post.html', 
                      {'post':post})



# 작업중
def write(request):
    if request.method == 'POST':
        post_title = request.POST.get('title')
        post_detail = request.POST.get('contents')
        member_id = request.session.get('member_id')
        # uploadedFile= request.FILES.getlist("image")
    
        now = datetime.datetime.now()
        
        a = Post(
            save_post_title = post_title,
            save_post_detail = post_detail,
            save_post_update = now,
            save_member_id = member_id,
        )
        a.save()
        # for uploadFile in uploadedFile:
        #     # image_name = 
        #     i = AlgorithmImage(
        #         image_name=uploadFile.name,
        #         image_root= "static/media/",
        #         algo_no=Algorithm.objects.get(algo_update=nowDate))
        #     i.save()
        #     save_path = os.path.join(STATIC_ROOT,i.image_name)
        #     with open(save_path, 'wb') as file:
        #         for chunk in uploadFile.chunks():
        #             file.write(chunk)
            
        # 글이 써지면 목록으로
        return render(request, 'board/postlist/')
        
    else:
        # get 메서드    
        
        return
    

def update(request, post_no):
    post = Post.objects.get(no=post_no)
    if request.method == "POST":
        post.title = request.POST['title']
        post.detail = request.POST['body']
        post.update = datetime.now()
        try:
            post.file = request.FILES['image']
        except:
            post.file = None
        post.save()
        return redirect('/post/'+str(post.no),{'post':post})
    else:
        post=Post()
        return render(request, 'update.html', {'post':post})




def delete(request, post_no):
    post = Post.objects.get(id=post_no)
    post.delete()
    return redirect('home')




def comment_write(request):
    
    return 

def comment_delete():
    return


def file():
    
    return 