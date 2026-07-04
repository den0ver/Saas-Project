from django.db import models
from apps.companies.models import Company


class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="customers")
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
