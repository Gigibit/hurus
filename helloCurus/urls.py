"""helloCurus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core import views as core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit_survey/', core.submit_survey),
    path('add_activity/', core.add_activity),
    path('tought_for_day/', core.tought_for_day),
    path('statistics_for_day/', core.statistics_for_day),
    path('statistics_manager_for_day/', core.statistics_manager_for_day),
    path('manager_tought_moods_count_in_day/', core.manager_tought_moods_count_in_day),
    path('manager_tought_moods_count/', core.manager_tought_moods_count_overview),
    path('statistics/', core.statistics),
    path('courses/', core.e_learning),
    path('curus/', core.happy_corus),
    path('send_contact_email/', core.send_contact_email),
    path('courses/<int:id>', core.e_learning_detail),
    path('login_with_token/<str:token>', core.login_user_from_token),
    path('website/', include('website.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', core.home),
]
