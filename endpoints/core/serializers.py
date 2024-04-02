from rest_framework import serializers
from core.models import Community

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['channel', 'name', 'owner_name']