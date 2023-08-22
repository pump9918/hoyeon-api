from django.http import HttpResponse
from rest_framework import viewsets
from .models import ttsPost, TTSAudioTitle, TTSAudio
from .serializers import ttsPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ttsPostViewSet(viewsets.ModelViewSet):
    queryset = ttsPost.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ttsPostSerializer
        return ttsPostSerializer
    
    def create(self, request, *args, **kwargs):
        return self.create_post_with_audio(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def create_post_with_audio(self, request):
        print(request.user) #로그인한 유저 확인용
        tts_title_message = request.data.get('tts_title_message')
        tts_message = request.data.get('tts_message')

        if not tts_title_message and not tts_message:
            return Response({"error": "tts_title_message 또는 tts_message 중 하나는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # request.data.copy()를 사용하여 수정 가능한 데이터 복사본을 만듭니다.
        data = request.data.copy()
        data['author'] = request.user.id

        post_serializer = ttsPostSerializer(data=data, context={'request': request})
        
        if post_serializer.is_valid():
            tts_title_message = request.data.get('tts_title_message')
            tts_message = request.data.get('tts_message')

            existing_tts_title = None
            existing_tts_audio = None

            if tts_title_message:
                existing_tts_titles = TTSAudioTitle.objects.filter(title_message=tts_title_message, user=request.user)
                if existing_tts_titles.exists():
                    existing_tts_title = existing_tts_titles.first()

            if tts_message:
                existing_tts_audios = TTSAudio.objects.filter(message=tts_message, user=request.user)
                if existing_tts_audios.exists():
                    existing_tts_audio = existing_tts_audios.first()

            post = post_serializer.save(author=request.user)

            if existing_tts_title:
                post.tts_title_audio = existing_tts_title
            if existing_tts_audio:
                post.tts_audio = existing_tts_audio
            
            post.save()

            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TTSAudioTitleAPIView(APIView):
    permission_classes = []
    
    def get(self, request, pk=None):
        post = ttsPost.objects.get(pk=pk)
        if post.tts_title_audio:
            file_path = post.tts_title_audio.audio_file.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="tts_title_{post.id}.mp3"'
                return response
        return Response({'message': '음성 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

class TTSAudioAPIView(APIView):
    permission_classes = []
    
    def get(self, request, pk=None):
        post = ttsPost.objects.get(pk=pk)
        if post.tts_audio:
            file_path = post.tts_audio.audio_file.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="tts_{post.id}.mp3"'
                return response
        return Response({'message': '음성 파일이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)