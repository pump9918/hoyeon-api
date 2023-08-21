from django.contrib import admin
from .models import ttsPost, TTSAudio, TTSAudioTitle

@admin.register(ttsPost)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(TTSAudioTitle)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(TTSAudio)
class PostModelAdmin(admin.ModelAdmin):
    pass
