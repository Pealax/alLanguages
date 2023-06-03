from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class UserChallengeSet(viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'put', 'patch', 'head']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ChallengeUpdateSerializer
        return ChallengeSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Challenge.objects.filter(user_id=user_id, state='Proceed', remainder__gt=0)

    def partial_update(self, *args, **kwargs): # 'patch' makes Challenge inactive  
        instance = self.get_queryset().get(id=kwargs.get('pk'))
        serializer = ChallengeSerializer(instance, data={'is_active': False}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserChallengeHistory(ListAPIView):

    serializer_class = ChallengeHistorySerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Challenge.objects.filter(user_id=user_id).exclude(state='Proceed')