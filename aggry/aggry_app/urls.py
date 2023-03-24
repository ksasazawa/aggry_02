from django.urls import path
from . import views

app_name = 'aggry_app'

urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('home', views.home, name="home"),
    path('job_detail/<int:id>/', views.job_detail, name="job_detail"),
    path('test', views.test, name="test"),
]