import os
from gtts import gTTS
from django.conf import settings
from rest_framework import serializers
from .models import ttsPost, TTSAudio, TTSAudioTitle


class TTSAudioTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSAudioTitle
        fields = '__all__'
        
class TTSAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSAudio
        fields = '__all__'


class ttsPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.email', read_only=True)
    tts_title_audio_message = serializers.CharField(source='tts_title_audio.title_message', read_only=True)
    tts_audio_message = serializers.CharField(source='tts_audio.message', read_only=True)
    
    class Meta:
        model = ttsPost
        fields = ('id', 'published_date', 'author', 'author_name', 'tts_title_message', 'tts_message', 'tts_title_audio', 'tts_audio', 'tts_title_audio_message', 'tts_audio_message')
        read_only_fields = ('id', 'published_date', 'author', 'author_name', 'tts_title_audio_message', 'tts_audio_message')

    def create(self, validated_data):
        tts_title_message = validated_data.pop('tts_title_message', None)
        tts_message = validated_data.pop('tts_message', None)
        
        author = self.context['request'].user
        
        if tts_title_message: 
            tts_title = gTTS(text=tts_title_message, lang='ko')
            tts_title_audio = TTSAudioTitle(title_message=tts_title_message, user=author)
            tts_title_audio.save()

            tts_folder = os.path.join(settings.MEDIA_ROOT, 'tts_title')
            os.makedirs(tts_folder, exist_ok=True)

            save_path = os.path.join(tts_folder, f'tts_title_{tts_title_audio.id}.mp3')
            tts_title.save(save_path)

            tts_title_audio.audio_file = f'tts_title/tts_title_{tts_title_audio.id}.mp3'
            tts_title_audio.save()

            validated_data['tts_title_audio'] = tts_title_audio
            
        if tts_message:
            tts = gTTS(text=tts_message, lang='ko')
            tts_audio = TTSAudio(message=tts_message, user=author)
            tts_audio.save()

            tts_folder = os.path.join(settings.MEDIA_ROOT, 'tts')
            os.makedirs(tts_folder, exist_ok=True)

            save_path = os.path.join(tts_folder, f'tts_{tts_audio.id}.mp3')
            tts.save(save_path)

            tts_audio.audio_file = f'tts/tts_{tts_audio.id}.mp3'
            tts_audio.save()

            validated_data['tts_audio'] = tts_audio

        post = ttsPost.objects.create(**validated_data)
        return post