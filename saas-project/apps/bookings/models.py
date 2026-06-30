from django.db import models
from apps.companies.models import Company
from apps.services.models import Service
from apps.employees.models import Employee
from apps.customers.models import Customer

class Booking(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")

    date_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='pending')

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f"Booking Number: {self.id}"