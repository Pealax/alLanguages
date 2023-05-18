from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView
from word.models import Word
from rules.models import Question
from .models import *
from .serializers import *

class UserChallengeSet(viewsets.ModelViewSet):

    serializer_class = ChallengeSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Challenge.objects.filter(user_id=user_id, state='Active')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)