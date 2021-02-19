from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# from django.core.mail import mail_admins
from django.conf import settings
from accounts.models import Profile
# from django.contrib import messages 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()