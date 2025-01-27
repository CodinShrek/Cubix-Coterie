from django.urls import path
from . import views

urlpatterns = [
    path("/create", views.communitychatcreate_view, name='create'),
    path("/mychats", views.mychats, name='mymessages'),
    path("<slug>", views.mymessages_view, name='view-mymessages'),
    path("", views.commonview_chats, name='public forum')
    
    
]