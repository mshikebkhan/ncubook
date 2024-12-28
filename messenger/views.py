from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User

from .models import DM

def nav_dms_count(request):
    count = 0
    if request.user.is_authenticated:
        count = DM.objects.filter(receiver=request.user, seen=False).count()
        count = int(count/2) # As We Make 2 Copies Of A DM

    return {'nav_dms_count':count}

@login_required
def inbox(request):
    # Call It Chat As DM Clash With Django DMs
    dms = DM.objects.filter(owner=request.user).order_by('-date_created')
    dms_count = dms.count()
    dms_seen = DM.objects.filter(receiver=request.user).all()
    dms_seen.update(seen=True)

    context = {'inbox_link_active': "link-active", 'dms': dms, 'dms_count': dms_count}
    return render(request, 'messanger/dms.html', context)

@login_required
def send_dm(request):
    if request.method == "POST":

        # Collect Data From Ajax Form
        user_id = request.POST.get('user_id') 
        body = request.POST.get('body')

        # Create DM
        receiver = get_object_or_404(User, id=user_id)
        if receiver != request.user: # Can't Send Message To Yourself
            DM.objects.create(owner=request.user, sender=request.user, receiver=receiver, body=body[:100])                    

        return JsonResponse({'status': "Done"})
    else:
        raise Http404
        
@login_required
def delete_dm(request, dm_id):
    dm = DM.objects.get(id=dm_id)
    if request.method == "POST" and dm.owner == request.user:
        dm.delete() 
        return JsonResponse({'status': "Success"})
    else:
        raise Http404
