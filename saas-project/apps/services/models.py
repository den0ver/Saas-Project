from django.db import models
from apps.companies.models import Company


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['company', 'slug'], name="unique_service_slug")
        ]

    def __str__(self):
        return self.name


