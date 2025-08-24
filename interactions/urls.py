from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('like/<uuid:video_id>/', views.like_video, name='like_video'),
    path('dislike/<uuid:video_id>/', views.dislike_video, name='dislike_video'),
    path('comment/add/<uuid:video_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<uuid:comment_id>/', views.delete_comment, name='delete_comment'),
    path('view/<uuid:video_id>/', views.record_view, name='record_view'),
    path('ajax/toggle-like/<uuid:video_id>/', views.toggle_like_ajax, name='toggle_like_ajax'),
]