from django.urls import path
from django.contrib.auth import views as authViews 
from .import views

urlpatterns = [
    # Direct Messages Page
    path('inbox', views.inbox, name='inbox'), 

    # Send DM
    path('send_dm/', views.send_dm),

    # Delete DM
    path('delete_dm/<int:dm_id>/', views.delete_dm, name='delete_dm'),
]
