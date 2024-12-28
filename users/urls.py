from django.urls import path
from django.contrib.auth import views as authViews 
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # Sign Up Page    
    path('signup/', views.signup, name='signup'),

    # Password Reset Confirm
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),

    # Password Reset 
    path('password_reset/<int:user_id>/', views.password_reset, name='password_reset'),

    # Profile Page
    path('<str:username>/profile', views.profile, name='profile'), 

    # Buddies Page
    path('<str:user>/buddies', views.buddies, name='buddies'),

    # Remove Buddy 
    path('remove_buddy/<int:user_id>/', views.remove_buddy),

    # Send Buddy Request
    path('send_request/<int:user_id>/', views.send_request),

    # Accept Buddy Request
    path('accept_request/<int:request_id>/', views.accept_request),

    # Reject Buddy Request
    path('reject_request/<int:request_id>/', views.reject_request),

    # Buddy Requests Page
    path('buddy_requests', views.buddy_requests, name='buddy_requests'), 

    # Edit Profile Page
    path('edit_profile/', views.edit_profile, name='edit_profile'), 

    # Verify Account Link
    path('verify_account_link/', views.verify_account_link, name='verify_account_link'),

    # Verify Account 
    path('verify_account/', views.verify_account, name='verify_account'),

    # Login Details Page
    path('login_details/', views.login_details, name='login_details'),

    # Settings / Change Password Page
    path('settings/change_password/', views.change_password, name='change_password'),     
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)