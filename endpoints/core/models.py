from django.db import models
from datetime import datetime

class Community(models.Model):
    id_channel = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=40, blank=False)
    owner_name = models.CharField(max_length=40, default="")
    created_at = models.DateField(null=True)
    insert_data = models.DateField(auto_now=True)

    def __str__(self):
        return f"Community: {self.name} - {self.id_channel} - {self.owner_name}"
    

class Member(models.Model):
    
    class Meta:
        verbose_name_plural = "Members"

    id_member = models.CharField(max_length=50, unique=True)
    nick = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, blank=False)
    descriminator = models.CharField(max_length=15, null=True)
    is_bot = models.BooleanField(default=False)

    def __str__(self):
        return f"Member: {self.name} - Nick: {self.nick} - {self.descriminator} - Bot: {self.is_bot}"