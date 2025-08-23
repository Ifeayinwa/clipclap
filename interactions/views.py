from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from videos.models import Video
from .models import Like, Comment, View
from django.http import JsonResponse

@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        video=video,
        defaults={'is_like': True}
    )
    
    if not created:
        if like.is_like:
            like.delete()
            action = 'unliked'
        else:
            like.is_like = True
            like.save()
            action = 'liked'
    else:
        action = 'liked'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'like_count': video.like_count,
        })
    
    messages.success(request, f'You {action} the video.')
    return redirect('videos:watch', video_id=video_id)

@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')
        
        if text:
            parent = None
            if parent_id:
                parent = Comment.objects.get(id=parent_id)
            
            Comment.objects.create(
                user=request.user,
                video=video,
                text=text,
                parent=parent
            )
            messages.success(request, 'Comment added successfully!')
    
    return redirect('videos:watch', video_id=video_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    video_id = comment.video.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('videos:watch', video_id=video_id)

def record_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user.is_authenticated:
        viewer = request.user
    else:
        viewer = None
    
    View.objects.create(user=viewer, video=video)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'view_count': video.views.count(),
        })
    
    return redirect('videos:watch', video_id=video_id)
