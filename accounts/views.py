from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin

from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	TemplateView,
)

from accounts.models import Profile


from .forms import (
	UserRegisterForm,
	UserUpdateForm,
	ProfileUpdateForm,
	PlanForm
)

import requests

plans  = {'1': 'free', '2': 'standard', '3' : 'supercharged'}


class Plans(TemplateView):
	template_name = "frontend/pages/plans.html"

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('login'))
		
		form = PlanForm(request.POST or None) 

		if form.is_valid():
			obj = get_object_or_404(Profile, user=request.user)

			plan_choice_num = form.cleaned_data.get("plan")
			plan_choice = plans.get(plan_choice_num)
			print(plan_choice_num)
			print(plan_choice)

			obj.plan = plan_choice

			obj.save()

			return redirect(reverse('frontend:dashboard'))
		return redirect(reverse('plans'))


def profile(request, *args, **kwargs):

	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'frontend/pages/dashboard/profile.html', context)



def upgrade(request, *args, **kwargs):
	return render(request, 'frontend/pages/dashboard/upgrade.html',{})




def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			recaptcha_response = request.POST.get('g-recaptcha-response')
			data = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result = r.json()
			''' End reCAPTCHA validation '''
			if result['success']:
				user = form.save()
				# want_newsletter = form.cleaned_data.get('newsletter')

				# username = form.cleaned_data.get('username')
				
				# email = form.cleaned_data.get('email')

				# user.profile.want_newsletter = want_newsletter

				user.save()
				# if want_newsletter:
				# 	NewsLetter.objects.create(user=username,email=email)

				# User_Agreements.objects.create(user=user,want_newsletter=want_newsletter)
				username = form.cleaned_data.get('email')
				password = form.cleaned_data.get('password1')
				print(username)
				print(password)
				
				user_auth = authenticate(username=username, password=password)
				print(user_auth)
				login(request, user_auth)
				messages.success(request, f'Your account has been created! You are now able to log in')
				return redirect('plans')
			else:
				messages.warning(request, 'Invalid reCAPTCHA. Please try again.')
			
		else:
			messages.info(request, f'Something went wrong!!')

	else:
		
		form = UserRegisterForm()
	return render(request, 'frontend/pages/auth/register.html',{'form':form})






