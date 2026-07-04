from django.urls import path
from . import views 


app_name = "bookings"


urlpatterns = [
    path('', views.list_bookings, name="list"),
    path('create/', views.create_booking, name="create"),
    path('detail/<int:id>/', views.detail_booking, name="detail"),
    path('edit/<int:id>/', views.edit_booking, name="edit"),
    path('delete/<int:id>/', views.delete_booking, name="delete"),
] 