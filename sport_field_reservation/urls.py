"""sport_field_reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from sport_field_app.views import IndexView, SportFieldListView, SportFieldDetailsView, \
    EditSportFieldView, AddFieldView, DeleteSportFieldView, BookSportFieldView, \
    SearchView, CalendarView, ContactView
# from sport_field_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('sport-field-list/', SportFieldListView.as_view()),
    path('sport-field/<int:sport_field_id>/', SportFieldDetailsView.as_view()),
    path('add-sport-field/', AddFieldView.as_view()),
    path('sport-field/delete/<int:sport_field_id>/', DeleteSportFieldView.as_view()),
    path('sport-field/edit/<int:sport_field_id>/', EditSportFieldView.as_view()),
    path('sport-field/book/<int:sport_field_id>/', BookSportFieldView.as_view()),
    path('search/', SearchView.as_view()),
    path('calendar/', CalendarView.as_view()),
    path('contact/', ContactView.as_view()),
]
