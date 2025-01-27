from django.shortcuts import get_object_or_404, render, redirect
from .models import CommunityChat
from .forms import CommunityChatCreateForm
from user.models import Account
from django.contrib.auth.decorators import login_required
from operator import attrgetter
# Create your views here.

def communitychatcreate_view(request):
    
    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    form = CommunityChatCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        user = Account.objects.filter(firstname=request.user.firstname).first()
        if user:
            obj.user = user
            obj.save()
        
        
    context['form'] = form

    return render(request, "community/chat_post.html", context)

@login_required
def mychats(request):
    context={}
    community_chat = CommunityChat.objects.filter(user=request.user)
    context['community_chat'] = community_chat
    
    return render(request, "community/mychats.html", context)

def mymessages_view(request, slug):
	
	context = {}
	community_chat = get_object_or_404(CommunityChat, slug=slug)
	context['community_chat'] = community_chat

	return render(request, 'community/view_mymessages.html', context)

def commonview_chats(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    context={}
    community_chat = sorted(CommunityChat.objects.all(), key=attrgetter('video_details'), reverse=True)
    context['community_chat'] = community_chat
    
    return render(request, "community/publicforum.html", context)