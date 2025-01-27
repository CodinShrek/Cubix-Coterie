from django import forms
from community.models import CommunityChat

class CommunityChatCreateForm(forms.ModelForm):
    
    class Meta:
        model = CommunityChat
        fields = ["subject","content", "video"]
