from django.urls import path, include #
from rest_framework import routers #
from .views import *

router = routers.SimpleRouter()
router.register('', UserChallengeSet, basename='user-сhallenge')
#UserRulesSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('history/', UserChallengeHistory.as_view(), name='сhallenge-history'),
    path('', include(router.urls)) # Челендж
]