from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'study', QuestionsStudySet, basename='question-study') # вопросов для обучения'
router.register(r'question', UserQuestionsSet, basename='user-question') # вопросы 'в работе'

urlpatterns = [
    path('check/', UserQuestionsCheck.as_view(), name='question-check'), # 1 вопрос для проверки
    path('', include(router.urls))
]