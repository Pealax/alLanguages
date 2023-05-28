from django.urls import path, include
from rest_framework.routers import DefaultRouter
from word.views import WordViewSet, QueryList, Translates, update_progress

router = DefaultRouter()
router.register(r'', WordViewSet, basename='words')


urlpatterns = [
    path('w/progress/', update_progress),
    path('translates/<pk>/', Translates.as_view(), name='translates'),
    path('query/<pk>/', QueryList.as_view(), name='queries'),
    path('', include(router.urls))
]
