from django.urls import path
from . import views

urlpatterns = [
    path("", views.stopwatch, name="stopwatch"),
    path("/start", views.start_stopwatch, name = 'start'),
    path("/stop", views.stop_stopwatch, name = 'stop'),
    path("/history", views.history, name = 'table'),
    path("/result", views.result, name="result"),
    path("/leaderboard", views.display_first_duration, name="leaderboard"),
    path("/personalbests", views.personal_best, name="personalbests")
    
]