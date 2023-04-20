from django.urls import path
from rules.views import *

urlpatterns = [
    path('', RulesListView.as_view(), name='rules-list'),
    path('my/', UserRulesListView.as_view(), name='user-rules-answers-list'),
    path('my/checklist/', UserRulesVerifiesList.as_view(), name='user-rules-verify-list'),
    path('my/check/', UserRulesCheck.as_view(), name='user-rules-check'),
    path('my/correct/', UserRulesCorrectListView.as_view(), name='user-rule-correct-list'),
    path('my/correct/<int:pk>', UserRulesCorrect.as_view(), name='user-rule-correct'),
    path('my/delete/', UserRulesDeleteListView.as_view(), name='user-rule-delete-list'),
    path('my/delete/<int:pk>', UserRulesDelete.as_view(), name='user-rule-delete'),
]