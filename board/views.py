import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Post, Member, Comment, Postfile

# Create your views here.
def postlist(request):
    post_list = Post.objects.all()
    count = len(post_list)
    
    return render(
        request,
        'board/postlist.html',
        {'post_list': post_list, 'count':count,}
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
        save_post_title = request.POST.get('postname')
        save_post_detail = request.POST.get('contents')
        save_member_id = request.session.get('member_id')
        # uploadedFile= request.FILES.getlist("image")
        # save_member_id = 'Member object (test24)'
    
        now = datetime.datetime.now()
        
        a = Post(
            post_title = save_post_title,
            post_detail = save_post_detail,
            post_update = now,
            member_id = save_member_id,
        )
        a.save()
        # for uploadFile in uploadedFile:
        #     # image_name = 
        #     i = Postfile(
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
        
        return render(request, 'board/write.html')
    

def update(request, post_no):
    post = Post.objects.get(post_no=post_no)
    if request.method == "POST":
        post.post_title = request.POST['postname']
        post.post_detail = request.POST['contents']
        post.post_update = datetime.now()
        try:
            post.file = request.FILES['image']
        except:
            post.file = None
        post.save()
        return redirect('/post/'+str(post.no),{'post':post})
    else:
        post=Post.objects.get(post_no = post_no)
        return render(request, 'board/write.html', {'post':post})




def delete(request, post_no):
    post = Post.objects.get(post_no=post_no)
    post.delete()
    return postlist(request)







def comment_write(request, post_no):
    if request.method == 'POST':
        now = datetime.datetime.now()
        save_member_id = request.session.get('member_id')
        jsonObject = json.loads(request.body)
        t_post_no = jsonObject.get('post_no')
        reply = Comment.objects.create(
            # 
            save_post_no=Post.objects.get(post_no=t_post_no),
            save_member_id=Member.objects.get(member_id=save_member_id),
            comment_detail=jsonObject.get('comment_detail'),
            comment_update = now
        )
        reply.save()
        
        membername = Member.objects.get(member_id = save_member_id)
        context = {
            # 'name': serializers.serialize("json", reply.member_no),
            'content': reply.comment_detail,
            'pp': membername.member_nick,    
        }

        return JsonResponse(context)


# def comment_delete(request):
#     comment = Comment.objects.get(comment_no=comment_no)
#     post.delete()
#     return


def file():
    
    return 