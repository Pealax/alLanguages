from django.urls import path
from rules.views import *

urlpatterns = [
    path('', RulesListView.as_view(), name='rules-list'),
    path('<int:user_id>', UserRulesListView.as_view(), name='user-rules-answers-list'),
    path('<int:user_id>/checklist/', UserRulesVerifiesList.as_view(), name='user-rules-verify-list'),
    path('<int:user_id>/check/', UserRulesCheck.as_view(), name='user-rules-check'),
    path('<int:user_id>/correct/', UserRulesCorrectListView.as_view(), name='user-rule-correct-list'),
    path('<int:user_id>/correct/<int:pk>', UserRulesCorrect.as_view(), name='user-rule-correct'),
    path('<int:user_id>/delete/', UserRulesDeleteListView.as_view(), name='user-rule-delete-list'),
    path('<int:user_id>/delete/<int:pk>', UserRulesDelete.as_view(), name='user-rule-delete')
]