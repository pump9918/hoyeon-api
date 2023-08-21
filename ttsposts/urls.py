from django.urls import path
from rest_framework import routers
from .views import ttsPostViewSet, TTSAudioAPIView, TTSAudioTitleAPIView

app_name = 'ttsposts'

router = routers.SimpleRouter()
router.register('', ttsPostViewSet)

urlpatterns = [
    *router.urls,
    path('<int:pk>/tts_title_mp3/', TTSAudioTitleAPIView.as_view(), name='tts_title_mp3'),
    path('<int:pk>/tts_mp3/', TTSAudioAPIView.as_view(), name='tts-audio-api'),
]
