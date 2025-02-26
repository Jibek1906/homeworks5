import random
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_confirmation_code(self):
        self.confirmation_code = str(random.randint(100000, 999999))
        self.save()
        
        
    def __str__(self):
        return f"{self.user} - {self.confirmation_code}"