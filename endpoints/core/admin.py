from django.contrib import admin
from core.models import Community, Member

admin.site.site_title = admin.site.site_header = admin.site.index_title = "Discord API"

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("id_channel", "name", "owner_name", "created_at")
    search_fields = ("id_channel", "name", "owner_name")

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id_member", "name", "nick", "is_bot", "descriminator")
    list_filter = ("is_bot", )
    list_editable = ("is_bot", )
    search_fields = ("id_member", "name")