from django.contrib import admin
from .models import Like, Comment, View

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('user__username', 'video__title')
    readonly_fields = ('created_at',)
    list_editable = ('is_like',)
    
    fieldsets = (
        ('Like Information', {
            'fields': ('user', 'video', 'is_like', 'created_at')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'truncated_text', 'created_at', 'reply_count')
    list_filter = ('created_at', 'video')
    search_fields = ('user__username', 'video__title', 'text')
    readonly_fields = ('created_at', 'updated_at', 'reply_count')
    raw_id_fields = ('parent',)  # Useful for foreign keys to avoid loading all instances
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('user', 'video', 'text')
        }),
        ('Relationships', {
            'fields': ('parent',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Metrics', {
            'fields': ('reply_count',),
            'classes': ('collapse',)
        }),
    )

    def truncated_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    truncated_text.short_description = 'Comment Text'

    def reply_count(self, obj):
        return obj.reply_count
    reply_count.short_description = 'Replies'

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('video', 'user_display', 'created_at')
    list_filter = ('created_at', 'video')
    search_fields = ('video__title', 'user__username')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('View Information', {
            'fields': ('user', 'video', 'created_at')
        }),
    )

    def user_display(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    user_display.short_description = 'User'