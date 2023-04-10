from django.urls import path
from rules import views
from rules.views import RulesListView

urlpatterns = [
    path('', RulesListView.as_view(), name='rules-list'),
    path('index/', views.index),
    path('create/', views.create),
    path('check/', views.check),
    path('correct/', views.correct),
    path('delete/', views.delete),
]