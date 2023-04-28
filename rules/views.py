from django.db.models import Sum
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
        if self.action == 'update':
            return Question.objects.filter(user_id=user_id, status='RJ')
        else:
            return Question.objects.filter(user_id=user_id).exclude(status='AP')

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id,
                        native_id=self.request.user.native_id,
                        learn_id=self.request.user.learn_id)


class UserQuestionsCheck(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionCheckSerializer
        else:
            return CheckSerializer

    def get_queryset(self):
        user = self.request.user
        questionslist = Question.objects.filter(status='PR',
                native_id=user.native_id,
                learn_id=user.learn_id).exclude(user=user).exclude(check__user=user)
        return questionslist.order_by('?')[:1]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        question_id = serializer.data.get('question')
        question_now = Question.objects.get(id=question_id)
        checks_question = Check.objects.filter(question_id=question_id)
        sum = checks_question.aggregate(Sum('flag'))['flag__sum']
        count = len(checks_question)
        if count - sum >= 3:
            question_now.status = 'RJ'
            question_now.save()
        elif 2*sum - count >= 3:
            question_now.status = 'AP'
            question_now.save()