from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Announcement
from users.models import CoarseBranch
from posts.models import Post
from posts.forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.http import Http404

@login_required
def index(request):
    buddies = request.user.profile.buddies.all()
    announcement = Announcement.objects.last()
    posts = Post.objects.filter(user__in=list(buddies)).order_by('-date_created')[:100]
    form = PostForm()
    context = {'index_link_active': "link-active", 'announcement': announcement.body, 'posts': posts, 'form': form}
    return render(request, 'ncubook/index.html', context)

@login_required
def search(request):
    coarse_branches = CoarseBranch.objects.all()            
    context = {'search_link_active': "link-active", 'coarse_branches': coarse_branches}     
    if request.method == "POST":
        query = request.POST.get("q")
        query = query.lstrip(" ")
        query = query.rstrip(" ")
        first_name = query.split(" ")
        if len(query) > 1:
            users = User.objects.filter(profile__roll__icontains=query).order_by('-date_joined') | \
                    User.objects.filter(username__icontains=query).order_by('-date_joined') | \
                    User.objects.filter(first_name__icontains=first_name[0]).order_by('-date_joined') | \
                    User.objects.filter(last_name__icontains=query).order_by('-date_joined')
            context['query'] = str(query)        
            context['users'] = users
    return render(request, 'ncubook/search.html', context)

@login_required
def search_by_coarse_branch(request, coarse_branch):
    coarse_branch = coarse_branch
    coarse_branches = CoarseBranch.objects.all()
    users = User.objects.filter(profile__coarse_branch__title=coarse_branch).order_by('-date_joined')
    context = {'search_link_active': "link-active", 'coarse_branches': coarse_branches, 'users': users}
    return render(request, 'ncubook/search.html', context)

def privacy(request):
    """Privacy Policy page"""
    return render(request, 'ncubook/privacy.html')

def terms(request):
    """Terms & Conditions page"""
    return render(request, 'ncubook/terms.html')

def about(request):
    """About us page"""
    return render(request, 'ncubook/about.html')

def contact(request):
    """Contact us page (with message functionality)"""
    return render(request, 'ncubook/contact.html')

def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
        return redirect('ncubook:login')
    else:
        raise Http404    