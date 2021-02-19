from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Account,Profile

User = get_user_model()


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
	# newsletter = forms.BooleanField(label='subscribe to our newletter',required=False)

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2',)


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	image = forms.ImageField(
		label=('Image'),
		required=False,
		error_messages = {'invalid':("Image files only")},
		widget=forms.FileInput
	)
	class Meta:
		model = Profile
		fields =  ['phone_number','image']

class PlanForm(forms.Form):
	plan = forms.CharField(max_length=225)