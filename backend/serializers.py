from backend.models import Schedule
from rest_framework import serializers


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    date = serializers.DateTimeField(format="iso-8601", required=True)
    class Meta:
        model = Schedule
        fields = ['url', 'id', 'user', 
                  'title', 'message', 'date','flair','medium', 'peoples_to_send']