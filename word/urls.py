from django.urls import path, include
from rest_framework.routers import DefaultRouter
from word.views import *

router = DefaultRouter()
router.register(r'', WordViewSet, basename='words')

urlpatterns = [
    path('progress/', ProgressList.as_view(), name='progress-list'),
    path('translates/', TranslatesList.as_view(), name='translates-list'),
    path('', include(router.urls))
]