from django.urls import path
from . import views


app_name = 'customers'


urlpatterns = [
    path('', views.list_customers, name="list"),
    path('create/', views.create_customer, name="create"),
    path('detail/<int:id>/', views.detail_customer, name="detail"),
    path('edit/<int:id>/', views.edit_customer, name="edit"),
    path('delete/<int:id>/', views.delete_customer, name="delete")
]