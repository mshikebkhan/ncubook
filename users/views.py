from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm, ChangePasswordForm, PasswordResetForm, ProfileUpdateForm, AccountVerifyForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Profile, BuddyRequest
from notifications.models import Notification
from posts.models import Post
from django.core.mail import send_mail
import random


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Split Name In First Name & Last Name
            name = name.split(" ")
            first_name = name[0]

            # Extract Last Name In String Form
            raw_last_name = name[1:]
            last_name = ""
            for ele in raw_last_name:
                last_name += ele + " "
           
            new_user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username.lower(), password=password)

            # create_profile(new_user)
            Profile.objects.create(user=new_user)
            
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(
                request, f'{first_name}, You are most welcome on NCUbook! please complete your profile.')
            return redirect('users:edit_profile')

        else:
            messages.error(
                request, f'Unable to create  account! Please correct the errors below.')            

    else:
        form = SignUpForm()

    context = {'form': form}

    return render(request, 'users/signup.html', context)

def password_reset_confirm(request):
    context = {} # For Get Request
    if request.method == "POST":
        username = request.POST.get("username")
        context['username'] = username
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_id = user.id

            # Generate & Save OTP
            raw_otp = random.randint(1000, 9999)
            user.profile.otp = raw_otp
            user.profile.save()

            # Send OTP Email
            recipient_list = [user.profile.email,]
            send_mail(
                "OTP for NCUbook password reset.",
                f"OTP: {str(raw_otp)} (Ignore if you did not requested this.)",
                "NCUBook",
                recipient_list,
                fail_silently=True,
            )              

            messages.success(
                request, f'OTP has been sent on your NCU email adress.')
            return redirect('users:password_reset', user_id=user_id) # Redrct For Further Prcss
        else:
            messages.error(
                request, f'We did not found any account this username.')                   

    return render(request, 'users/password_reset_confirm.html', context)

def password_reset(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        profile = user.profile
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            new_password = form.cleaned_data.get('new_password')
            if otp == profile.otp and otp != 0:
                profile.otp = 0 # Reset OTP
                profile.save()
                user.set_password(new_password)
                user.save()
                authenticated_user = authenticate(username=user.username,
                                                  password=request.POST['new_password'])
                login(request, authenticated_user) # Login User With New Password               
                messages.success(
                request, f'Password has been resetted successfully.')
                return redirect('ncubook:index')
            else:            
                messages.error(
                request, f'Incorrect OTP! Please enter correct OTP')

        else:
            messages.error(
                request, f' Unable to reset password. Please correct the error below.')
    else:
        form = PasswordResetForm()
    
    context = {'form': form,}
    return render(request, 'users/password_reset.html', context)

@login_required
def edit_profile(request):
    """ Settings Page / Edit profile """
    profile = request.user.profile
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()

            # Detect Change In Verified Roll No (User Have To Verify Again!)
            if profile.roll != profile.verified_roll:
                profile.verified = False
                profile.save()

            messages.success(
                request, f'Profile has been updated successfully.')
            return redirect('users:profile', username=request.user.username)
        else:
            messages.error(
                request, f' Unable to update profile. Please correct the error below.')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'uform': uform,
        'pform': pform
    }

    return render(request, 'users/edit_profile.html', context)

@login_required
def verify_account_link(request):
    return render(request, 'users/verify_account_link.html')

@login_required
def verify_account(request):
    profile = request.user.profile

    if not profile.verified:
        # Generate & Save OTP
        raw_otp = random.randint(1000, 9999)
        profile.otp = raw_otp
        profile.save()

        # Send OTP Email
        recipient_list = [profile.email,]
        send_mail(
            "OTP for NCUbook roll no. verification.",
            f"OTP: {str(raw_otp)}",
            "NCUBook",
            recipient_list,
            fail_silently=True,
        )            

        if request.method == 'POST':
            form = AccountVerifyForm(request.POST)

            if form.is_valid():
                otp = form.cleaned_data.get('otp')
                if otp == profile.otp and otp != 0:
                    profile.verified = True
                    profile.otp = 0
                    profile.verified_roll = profile.roll # Verified Roll
                    profile.save()
                    messages.success(
                    request, f'Account has been verified successfully.')
                    return redirect('users:profile', username=profile.user.username)
                else:            
                    messages.error(
                    request, f'Incorrect OTP! Please enter correct OTP')

            else:
                messages.error(
                    request, f' Unable to verify account. Please correct the error below.')
        else:
            form = AccountVerifyForm()
        
        context = {'form': form,}

        return render(request, 'users/verify_account.html', context)
    else:
        return HttpResponse("Account is already verified")

@login_required
def profile(request, username):
    profile = Profile.objects.get(user__username=username)
    posts = Post.objects.filter(user=profile.user).order_by('-date_created')
    posts_count = posts.count()
    buddies_count = profile.buddies.all().count()
    context = {'profile_link_active': "link-active", 'profile': profile, 'posts': posts, 
    'posts_count': posts_count, 'buddies_count': buddies_count}
    return render(request, 'users/profile.html', context)

@login_required
def buddies(request, user):
    mutual_buddies_count = 0
    profile = Profile.objects.get(user__username=user)
    buddies = profile.buddies.all()
    print(buddies)
    buddies_count = buddies.count()

    my_buddies = request.user.profile.buddies.all()
    print(my_buddies)
    for my_buddy in my_buddies:
        if my_buddy in buddies:
            mutual_buddies_count += 1

    context = {'profile_link_active': "link-active", 'buddies': buddies, 'profile_user': profile.user.username,
     'buddies_count': buddies_count, 'mutual_buddies_count': mutual_buddies_count}
    return render(request, 'users/buddies.html', context)

@login_required
def remove_buddy(request, user_id):
    # Remove User From Buddies
    if request.method == "POST":
        user = request.user
        buddy = User.objects.get(id=user_id)
        response_data = {}

        # Remove Buddy From User's Buddies
        user.profile.buddies.remove(buddy)
        user.profile.save()
        # Remove User From Buddy's Buddies
        buddy.profile.buddies.remove(user)
        buddy.profile.save()
        response_data['status'] = 'done'
        return JsonResponse(response_data)
    else:
        raise Http404

def nav_brequests_count(request):
    count = 0
    if request.user.is_authenticated:
        count = BuddyRequest.objects.filter(receiver=request.user, seen=False).count()

    return {'nav_brequests_count':count}

@login_required
def send_request(request, user_id):
    # Send Buddy Request
    if request.method == "POST":
        response_data = {}
        sender = request.user
        receiver = User.objects.get(id=user_id)
        
        if not BuddyRequest.objects.filter(sender=sender, receiver=receiver).exists() and sender != receiver:
            BuddyRequest.objects.create(sender=sender, receiver=receiver)
            # Add Reciever In Sender's Requested 
            sender.profile.requested.add(receiver)
            sender.profile.save()
            response_data['status'] = 'sent'
        else:
            response_data['status'] = 'error'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def accept_request(request, request_id):
    # Accept Buddy Request
    if request.method == "POST":
        profile = request.user.profile
        response_data = {}
        brequest = BuddyRequest.objects.get(id=request_id)
        brequest.sender.profile.buddies.add(request.user) # Add In Reciver
        profile.save()
        request.user.profile.buddies.add(brequest.sender) # Add In Sender
        request.user.profile.save()
        # Remove Reciever From Sender's Requested 
        brequest.sender.profile.requested.remove(profile.user)
        brequest.sender.profile.save()
        # Delete Buddy Request
        brequest.delete()
        response_data['status'] = 'done'

        print("done")
        # Add Notification
        Notification.objects.create(sender=request.user, user=brequest.sender, notification_type=3)

        return JsonResponse(response_data)

    else:
        raise Http404

@login_required
def reject_request(request, request_id):
    # Delete Buddy Request
    if request.method == "POST":
        profile = request.user.profile
        response_data = {}
        request = BuddyRequest.objects.get(id=request_id)

        # Remove Reciever From Sender's Requested 
        request.sender.profile.requested.remove(profile.user)
        request.sender.profile.save()
        # Delete Buddy Request
        request.delete()
        response_data['status'] = 'done'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def buddy_requests(request):
    buddy_requests = BuddyRequest.objects.filter(receiver=request.user).order_by('-date_created')
    buddy_requests_count = buddy_requests.count()
    buddy_requests.update(seen=True)
    context = {'buddy_requests_link_active': "link-active", 'buddy_requests': buddy_requests, 'buddy_requests_count': buddy_requests_count}
    return render(request, 'users/buddy_requests.html', context)

@login_required
def login_details(request):
    """ Shows last login """
    user = request.user
    last_login = user.last_login
    context = {'last_login': last_login}
    return render(request, 'users/login_details.html', context)           

@login_required
def change_password(request):
    """ Change Password """
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            authenticated_user = authenticate(username=request.user.username,
                                              password=request.POST['new_password'])
            login(request, authenticated_user)
            messages.success(
                request, 'Your password has been updated successfully.')

            return redirect('users:settings')
        else:
            old_password = form.data.get('old_password')
            messages.error(
                request, f'Unable to update the password! Please correct the errors below.')
            
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'title': "Change Password", 'form': form
    }

    return render(request, 'users/change_password.html', context)     