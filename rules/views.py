from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from .models import *
from .serializers import *


class QuestionsStudySet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve': 
            return CategoryQuestionSerializer
        return CategorySerializer

    queryset = Category.objects.all()


class UserQuestionsSet(viewsets.ModelViewSet):

    serializer_class = QuestionAnswersSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Question.objects.filter(user_id=user_id)
        if self.action == 'update' or self.action == 'partial_update':
            queryset = queryset.filter(status='Reject')
        else:
            queryset = queryset.exclude(status='Complete')
        return queryset


class UserQuestionsCheck(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionCheckSerializer
        return CheckSerializer

    def get_queryset(self):
        user = self.request.user
        questionslist = Question.objects.filter(status='Proceed',
                native_id=user.native_id,
                learn_id=user.learn_id).exclude(user=user).exclude(check__user=user)
        return questionslist.order_by('?')[:1]