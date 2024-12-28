from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment
from notifications.models import Notification
from .forms import PostForm
from django.http import HttpResponse, JsonResponse, Http404

@login_required
def add_post(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Keep Only 5 Posts
            posts = Post.objects.filter(user=user)
            posts_count = posts.count()
            if posts_count >= 5:
                post = Post.objects.filter(user=user).first()
                post.delete()

            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(
                request, 'Posted successfully.')
        else:
            messages.error(
                request, 'Posted unsuccessfully.')
        return redirect('ncubook:index')

@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        preview = post.body[:70] #For noti.
        profile = request.user.profile

        # Like
        if post not in profile.liked_posts.all():
            post.likes += 1
            post.save() 
            profile.liked_posts.add(post)
            profile.save()

            # Add Notification
            if post.user != request.user:
                Notification.objects.create(post=post, sender=request.user, user=post.user, preview=preview, notification_type=1)

            
        # Unlike
        else:
            post.likes -= 1
            post.save() 
            profile.liked_posts.remove(post)
            profile.save()

            # Delete Notification
            if post.user != request.user:
                noti = Notification.objects.filter(post=post, sender=request.user, user=post.user, preview=preview, notification_type=1)
                noti.delete()

        return JsonResponse({'status': "Success"})
    else:
        raise Http404

@login_required
def report_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST" and post.user != request.user:
        post.reported = True
        post.save() 
        return JsonResponse({'status': "Success"})
    else:
        raise Http404

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST" and post.user == request.user:
        post.delete() 
        return JsonResponse({'status': "Success"})
    else:
        raise Http404

@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date_created')
    context = {'post': post, 'comments': comments}
    return render(request, 'posts/post_comments.html', context)

@login_required
def add_comment(request):
    if request.method == "POST":

        # Collect Data From Ajax Form
        post_id = request.POST.get('post_id') 
        body = request.POST.get('body')
        post = get_object_or_404(Post, id=post_id)

        # Keep Only 100 Comments
        comments = Comment.objects.filter(post=post)
        comments_count = comments.count()
        if comments_count >= 100:
            comment = Comment.objects.filter(post=post).first()
            comment.delete()

        # Create Comment
        Comment.objects.create(post=post, user=request.user, body=body[:100])                    

        # Add Notification
        if post.user != request.user:
            preview = body[:70] #For noti.
            Notification.objects.create(post=post, sender=request.user, user=post.user, preview=preview, notification_type=2)

        return JsonResponse({'status': "Success"})
    else:
        raise Http404

@login_required
def report_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST" and comment.user != request.user:
        comment.reported = True
        comment.save() 
        return JsonResponse({'status': "Success"})
    else:
        raise Http404

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST" and comment.user == request.user:
        comment.delete()

        # Delete Notification
        if post.user != request.user:
            noti = Notification.objects.filter(post=post, sender=request.user, user=post.user, preview=preview, notification_type=2)
            noti.delete() 
                    
        return JsonResponse({'status': "Success"})
    else:
        raise Http404



