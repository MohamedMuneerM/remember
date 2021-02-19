from django.urls import path
from frontend.views import (
	dashboard,
	# login,
	landing,
)

app_name = "frontend"

urlpatterns = [
    path('', landing, name="landing"),
    # path('login/', login, name="login"),
    # path('register/', register, name="register"),
    path('dashboard/', dashboard, name="dashboard"),
]