from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *

class UserChallengeSet(viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'put', 'head']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ChallengeUpdateSerializer
        return ChallengeSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Challenge.objects.filter(user_id=user_id, state='Active')


class UserChallengeHistory(ListAPIView):

    serializer_class = ChallengeHistorySerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Challenge.objects.filter(user_id=user_id).exclude(state='Active')