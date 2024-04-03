from rest_framework import serializers
from core.models import Community, Member

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id_channel', 'name', 'owner_name', 'created_at', 'insert_data']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id_member', 'name', 'descriminator', 'is_bot']

