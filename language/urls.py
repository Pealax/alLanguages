from django.urls import path

from language.views import LanguageListView

urlpatterns = [
    path('', LanguageListView.as_view(), name='languages-list'),
]
