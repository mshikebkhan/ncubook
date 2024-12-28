from django.urls import path
from django.contrib.auth import views as authViews 
from .import views

urlpatterns = [

    # Log In Page
    path('login/', authViews.LoginView.as_view(
        template_name='ncubook/login.html'), name='login'),
    
    # Home Page
    path('', views.index, name='index'), 
    
    # Search
    path('search/', views.search, name='search'),

    # Search By Coarse Branch
    path('search/<str:coarse_branch>/', views.search_by_coarse_branch, name='search_by_coarse_branch'),

    # Privacy Policy  Page 
    path('privacy/', views.privacy, name='privacy'),

    # Terms & Conditions  Page
    path('terms/', views.terms, name='terms'),

    # About us Page
    path('about/', views.about, name='about'),

    # Contact us Page
    path('contact/', views.contact, name='contact'),
        
    # Log Out Page
    path('logout/', views.logout, name='logout'),    
]
