from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .models import *
from .serializers import *


class QuestionsStudyList(ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        questionslist = Question.objects.filter(status='AP',
                native_id=user.native_id,
                learn_id=user.learn_id).exclude(user_id=user.id)
        return questionslist.order_by('?')[:10]


class UserQuestionsSet(viewsets.ModelViewSet):

    serializer_class = QuestionAnswersSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Question.objects.filter(user_id=user_id)
        if self.action == 'update' or self.action == 'partial_update':
            queryset = queryset.filter(status='RJ')
        else:
            queryset = queryset.exclude(status='AP')
        return queryset


class UserQuestionsCheck(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionCheckSerializer
        return CheckSerializer

    def get_queryset(self):
        user = self.request.user
        questionslist = Question.objects.filter(status='PR',
                native_id=user.native_id,
                learn_id=user.learn_id).exclude(user=user).exclude(check__user=user)
        return questionslist.order_by('?')[0]