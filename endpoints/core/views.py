from rest_framework import permissions, viewsets
from core.serializers import CommunitySerializer, MemberSerializer, ChannelSerializer
from core.models import Community, Member, Channel


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        community_id = self.request.data.get('community_id')
        serializer.save(community_id=community_id)