from django.urls import path
from .views import try_recent_audio, accept_media

urlpatterns = [
    path('accept_media/', accept_media, name='accept_media'),
    path('', try_recent_audio, name='home'),
]