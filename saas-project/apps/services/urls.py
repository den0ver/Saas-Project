from django.urls import path
from . import views 


app_name = "services"


urlpatterns = [
    path('', views.list_services, name='list'),
    path('create/', views.create_service, name='create'),
] 