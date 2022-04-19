from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # 글목록
    path('postlist/', views.postlist, name='postlist'),
     
    # 글 페이지
    path('post/<int:post_no>/', views.post, name='post'),
    
    
    # 글 crud
   
    path('post/write/', views.write, name='write'),
    path('board/post/', views.post, name='post'),
    path('post/<int:post_no>/update/',views.update, name="update"),
    path('post/<int:post_no>/delete/',views.delete, name="delete"),
    
    
]