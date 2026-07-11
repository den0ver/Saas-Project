from django.urls import path
from . import views 


app_name = "bookings"


urlpatterns = [
    path('', views.list_bookings, name="list"),
    path('create/', views.create_booking, name="create"),
    path('detail/<int:id>/', views.detail_booking, name="detail"),
    path('edit/<int:id>/', views.edit_booking, name="edit"),
    path('delete/<int:id>/', views.delete_booking, name="delete"),
    path('book/<slug:company_slug>/', views.public_booking, name="public_booking"),
    path('created/', views.created_booking, name="created"),
    path('book/<slug:company_slug>/slots/', views.get_slots, name="get_slots"),
] 