from django.urls import path
from rules.views import *

urlpatterns = [
    path('study/', RulesStudyList.as_view(), name='my-rules-list'), # 10 вопросов для обучения
    path('check/', UserRulesCheck.as_view(), name='user-rules-check'), # 1 вопрос для проверки
    path('my/',
        UserRulesSet.as_view({'get': 'list', 'post': 'create'}),
        name='user-rule-list-create'
    ), # вопросы 'в работе' список, создание
    path('my/<int:pk>',
        UserRulesSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='user-rule-upd-del'
    ), # вопросы 'в работе' корректировка, удаление
]