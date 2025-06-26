from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    student = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    counselor = models.ForeignKey(User, related_name='counselor_appointments', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        counselor_name = self.counselor.username if self.counselor else "Unassigned"
        return f"{self.student} with {counselor_name} on {self.date} at {self.time}"
