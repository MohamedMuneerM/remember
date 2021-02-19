from django.shortcuts import render
from backend.models import Schedule
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from backend.serializers import ScheduleSerializer
from backend.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    # queryset = Schedule.objects.filter()
    serializer_class = ScheduleSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)
