from django.contrib import admin
from django.urls import include, path
from website import views as site

urlpatterns = [
    path('', site.index),
]
