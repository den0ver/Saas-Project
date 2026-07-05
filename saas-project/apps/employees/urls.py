from django.urls import path
from . import views


app_name = "employees"


urlpatterns = [
    path('', views.list_employees, name="list"),
    path('create/', views.create_employee, name="create"),
    path('detail/<int:id>/', views.detail_employee, name="detail"),
]