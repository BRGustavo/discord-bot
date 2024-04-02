from django.db import models
from datetime import date

class Community(models.Model):
    channel = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=40, blank=False)
    owner_name = models.CharField(max_length=40, default="")
    insert_data = models.DateField(auto_now=True)

    def __str__(self):
        return f"Community: {self.name} - {self.channel} - {self.owner_name}"