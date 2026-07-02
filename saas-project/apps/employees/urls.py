from django.urls import path
from . import views


app_name = "employees"


urlpatterns = [
    path('', views.list_employees, name="list_employees"),
    path('create/', views.create_employee, name="create_employee"),
    path('detail/<int:id>/', views.detail_employee, name="detail_employee"),
]