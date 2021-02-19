from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.storage import default_storage as storage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from PIL import Image,ExifTags
import sys



class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError(_('Users must have an email address'))
		if not username:
			raise ValueError(_('Users must have a username'))

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def email_user(self, subject, message, from_email=None, **kwargs):
		'''
		Sends an email to this User.
		'''
		send_mail(subject, message, from_email, [self.email], **kwargs)

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


plans = [
	('free','Free'),
	('standard','Standard'),
	('supercharged', 'Super Charged')
]


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	image = models.ImageField(default='https://res.cloudinary.com/munokitchen/image/upload/v1606644051/default_image_txvds7.png',upload_to='profile_pics')
	want_newsletter = models.BooleanField(default=False)
	is_agreed_terms_and_conditions = models.BooleanField(default=False)
	plan = models.CharField(choices=plans, default="free", max_length=30)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)


	def __str__(self):
		return f'{self.user.username} Profile'

	# @property
	# def get_token(self):
	# 	return Token.objects.get(user=self.user) 

	@property
	def get_photo_url(self):
		if self.image and hasattr(self.image, 'url'):
			return self.image.url
		else:
			return "https://res.cloudinary.com/munokitchen/image/upload/v1606644051/default_image_txvds7.png"

	def get_rotation_code(self,img):

		if not hasattr(img, '_getexif') or img._getexif() is None:
			return None

		for code, name in ExifTags.TAGS.items():
			if name == 'Orientation':
				orientation_code = code
				break
		else:
			raise Exception('Cannot get orientation code from library.')

		return img._getexif().get(orientation_code, None)


	def rotate_image(self,img, rotation_code):
		if rotation_code == 1:
			return img
		if rotation_code == 3:
			img = img.transpose(Image.ROTATE_180)
		elif rotation_code == 6:
			img = img.transpose(Image.ROTATE_270)
		elif rotation_code == 8:
			img = img.transpose(Image.ROTATE_90)
		else:
			pass
		return img


	def save(self, *args, **kwargs):
		imageTemproary = Image.open(self.image)
		rotation_code = self.get_rotation_code(imageTemproary)
		if rotation_code is not None:
			imageTemproary = self.rotate_image(imageTemproary, rotation_code)
		outputIoStream = BytesIO()
		imageTemproaryResized = imageTemproary.resize( (300,300) ) 
		imageTemproaryResized.save(outputIoStream , format='PNG', quality=100)
		outputIoStream.seek(0)
		self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		try:
			super(Profile, self).save(*args, **kwargs)
		except Exception as e:
			pass

