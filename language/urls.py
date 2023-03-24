from django.urls import path
from language import views

from language.views import LanguageListView

urlpatterns = [
    path('', LanguageListView.as_view(), name='languages-list'),
    path('index/', views.index),
    path('create/', views.create),
]
