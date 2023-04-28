from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('', UserQuestionsSet, basename='user-question') # вопросы 'в работе'

urlpatterns = [
    path('study/', QuestionsStudyList.as_view(), name='study-questions-list'), # 10 вопросов для обучения
    path('check/', UserQuestionsCheck.as_view(), name='check-question'), # 1 вопрос для проверки
    path('my/', include(router.urls))
]