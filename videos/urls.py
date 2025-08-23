from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('upload/', views.upload_video, name='upload'),
    path('watch/<uuid:video_id>/', views.watch_video, name='watch'),
    path('edit/<uuid:video_id>/', views.edit_video, name='edit'),
    path('delete/<uuid:video_id>/', views.delete_video, name='delete'),
    path('search/', views.search, name='search'),
    path('tag/<slug:tag_slug>/', views.videos_by_tag, name='tag'),
]
