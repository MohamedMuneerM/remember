from django.db import models
from django.conf import settings
from django.utils import timezone


FLAIR = [
    ('birthday', 'Birthday'),
    ('anniversery', 'Anniversery'),
    ('meeting', 'Meeting'),
    ('special_day', 'Special Day'),
    ('other', 'Other'),
]

MEDIUM = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('both', 'Both'),   
]




class Schedule(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	title = models.CharField(max_length=199)
	message = models.TextField(blank=True, null=True)
	date = models.DateTimeField()
	flair = models.CharField(choices=FLAIR, default='birthday', max_length=30)
	medium =  models.CharField(choices=MEDIUM, default="email", max_length=30)
	peoples_to_send = models.JSONField(default=list, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created"]