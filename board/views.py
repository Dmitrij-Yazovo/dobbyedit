import datetime
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Post, Member, Comment, Postfile

# Create your views here.
def postlist(request):
    page = request.GET.get('page', '1')
    search_keyword = request.GET.get('keyword', '')
    search_type = request.GET.get('type', '')
    post_list = Post.objects.all()
    
    if search_type == 'all':
        post_list = post_list.filter(Q(post_title__icontains=search_keyword) |
                                    Q(post_detail__icontains=search_keyword) |
                                    Q(member_id__member_id__icontains=search_keyword)
                                    )
    elif search_type == 'post_title':
        post_list = post_list.filter(post_title__icontains=search_keyword)    
    elif search_type == 'post_detail':
        post_list = post_list.filter(post_detail__icontains=search_keyword)    
    elif search_type == 'member_id':
        post_list = post_list.filter(member_id__member_id__icontains=search_keyword)
    
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    print(page_obj)

    count = len(post_list)
    context = {'post_list': page_obj, 'page': page, 'keyword': search_keyword }
    
    return render(request, 'board/postlist.html', context)

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
        s_id = request.session.get('s_id')
        save_member_id = Member.objects.get(member_id=s_id)
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
        return redirect('/board/postlist/')
        
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
        s_id = request.session.get('s_id')
        jsonObject = json.loads(request.body)
        # t_post_no = jsonObject.get('post_no')
        reply = Comment.objects.create(
            # 
            post_no=Post.objects.get(post_no=post_no),
            member_id=Member.objects.get(member_id=s_id),
            comment_detail=jsonObject.get('comment_detail'),
            comment_update = now
        )
        reply.save()
        
        membername = Member.objects.get(member_id = s_id)
        context = {
            # 'name': serializers.serialize("json", reply.member_no),
            'content': reply.comment_detail,
            'pp': membername.member_nick    
        }

        return JsonResponse(context)


# def comment_delete(request):
#     comment = Comment.objects.get(comment_no=comment_no)
#     post.delete()
#     return


def file():
    
    return 