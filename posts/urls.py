from django.urls import path
from django.contrib.auth import views as authViews 
from .import views

urlpatterns = [

    # Add Post
    path('add_post/', views.add_post, name='add_post'), 

    # Like Post
    path('like_post/<int:post_id>/', views.like_post),

    # Report Post
    path('report_post/<int:post_id>/', views.report_post),

    # Delete Post
    path('delete_post/<int:post_id>/', views.delete_post),

    # Post Comments Page
    path('post_comments/<int:post_id>/', views.post_comments, name='post_comments'), 

    # Report Comment
    path('report_comment/<int:comment_id>/', views.report_comment),

    # Add Comment
    path('add_comment/', views.add_comment), 

    # Delete Comment
    path('delete_comment/<int:comment_id>/', views.delete_comment),    
]
