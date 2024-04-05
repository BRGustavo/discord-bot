from rest_framework import serializers
from core.models import Community, Member, Channel

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id','community', 'name', 'owner_name', 'created_at', 'insert_data']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id_member', 'name', 'descriminator', 'is_bot']

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["channel", "name", "topic", "is_news", "is_welcome_channel", "is_remove_channel", "is_role_channel"]

