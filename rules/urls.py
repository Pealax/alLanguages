from django.urls import path
from rules.views import *

urlpatterns = [
    path('', RulesListView.as_view(), name='all-rules-list'),
    path('my/', MyRulesListView.as_view(), name='my-rules-list'),
    path('current/', UserRulesCurrentList.as_view(), name='user-rules-current-list'),
    path('check/', UserRulesCheck.as_view(), name='user-rules-check'),
    path('upd/<int:pk>', UserRuleCorrect.as_view(), name='user-rule-correct'),
    path('del/<int:pk>', UserRuleDelete.as_view(), name='user-rule-delete'),
]