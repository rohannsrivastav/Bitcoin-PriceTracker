from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Alert(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('triggered', 'Triggered'),
        ('deleted', 'Deleted'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.CharField(max_length=10)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.cryptocurrency} - {self.target_price}"