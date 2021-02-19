from django.urls import path, include
from backend import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.ScheduleViewSet,'schedule')



urlpatterns = [
    path('', include(router.urls)),
]
