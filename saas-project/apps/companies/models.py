from django.db import models
from django.conf import settings


class Company(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    is_active = models.BooleanField(default=True)
    #subscription_until = models.DateField() (оплата подписки)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['owner', 'slug'], name="unique_company_slug")
        ]

    def __str__(self):
        return self.name
    

