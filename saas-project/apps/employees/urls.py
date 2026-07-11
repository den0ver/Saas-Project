from django.urls import path
from . import views


app_name = "employees"


urlpatterns = [
    path('', views.list_employees, name="list"),
    path('create/', views.create_employee, name="create"),
    path('detail/<int:id>/', views.detail_employee, name="detail"),
    path('edit/<int:id>/', views.edit_employee, name="edit"),
    path('delete/<int:id>/', views.delete_employee, name="delete"),
]