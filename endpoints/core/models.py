from django.db import models
from datetime import datetime

class Community(models.Model):
    community = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=40, blank=False)
    owner_name = models.CharField(max_length=40, default="")
    created_at = models.DateField(null=True)
    insert_data = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.community} - {self.name}"
    

class Channel(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    channel = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=255, default="Not set")
    created_at = models.DateTimeField(default=datetime.now)
    is_news = models.BooleanField(default=False)
    is_nsfw = models.BooleanField(default=False)

    is_welcome_channel = models.BooleanField(default=False)
    is_remove_channel = models.BooleanField(default=False)
    is_role_channel = models.BooleanField(default=False)
    
    position = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=(
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('category', 'Category')
    ), default="text")

    def __str__(self):
        return f"Community: {self.community.name} channel: {self.channel} name: {self.name}"

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