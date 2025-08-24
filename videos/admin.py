from django.contrib import admin
from .models import Video, Tag

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'visibility', 'created_at', 'like_count', 'comment_count')
    list_filter = ('visibility', 'created_at', 'tags')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at', 'like_count', 'comment_count')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'title', 'description')
        }),
        ('Media Files', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Visibility & Metadata', {
            'fields': ('visibility', 'tags', 'created_at', 'updated_at')
        }),
        ('Counts (Read-only)', {
            'fields': ('like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
    )

    def like_count(self, obj):
        return obj.like_count
    like_count.short_description = 'Likes'

    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'video_count')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Number of Videos'