from rest_framework import permissions, viewsets, status
from core.serializers import CommunitySerializer, MemberSerializer, ChannelSerializer
from core.models import Community, Member, Channel
from rest_framework.response import Response


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        community_id = request.query_params.get('community', None)
        
        if community_id:        
            try:
                community = Community.objects.get(community=community_id)
            except Community.DoesNotExist:
                return Response({"error": "Comunidade não encontrada."}, status=status.HTTP_404_NOT_FOUND)
            
            serialized_community = CommunitySerializer(community)
            return Response(serialized_community.data)
        else:
            communities = Community.objects.all()
            serialized_communities = CommunitySerializer(communities, many=True)
            return Response(serialized_communities.data)

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

    def list(self, request):
        community_id = request.query_params.get('community', None)
        
        if community_id:        
            channels = Channel.objects.filter(community__community=community_id)
            serialized_channels = ChannelSerializer(channels, many=True)
            return Response(serialized_channels.data)
        else:
            communities = Channel.objects.all()
            serialized_communities = ChannelSerializer(communities, many=True)
            return Response(serialized_communities.data)