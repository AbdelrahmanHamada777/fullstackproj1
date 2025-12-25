
from django.urls import path
from . import views


urlpatterns = [
    path('bot/', views.bot, name='bot'),  # صفحة الشات بوت
]