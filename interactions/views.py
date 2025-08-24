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
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        video=video,
        defaults={'is_like': False}
    )
    
    if not created:
        if not like.is_like:
            like.delete()
            action = 'undisliked'
        else:
            like.is_like = False
            like.save()
            action = 'disliked'
    else:
        action = 'disliked'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'like_count': video.like_count,
        })
    
    messages.info(request, f'You {action} the video.')
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
                try:
                    parent = Comment.objects.get(id=parent_id, video=video)
                except Comment.DoesNotExist:
                    messages.error(request, 'Parent comment not found.')
                    return redirect('videos:watch', video_id=video_id)
            
            Comment.objects.create(
                user=request.user,
                video=video,
                text=text,
                parent=parent
            )
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('videos:watch', video_id=video_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user owns the comment or is the video owner
    if comment.user != request.user and comment.video.user != request.user:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('videos:watch', video_id=comment.video.id)
    
    video_id = comment.video.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('videos:watch', video_id=video_id)

def record_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Check visibility before recording view
    if video.visibility == 'private' and video.user != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Private video'}, status=403)
        messages.error(request, 'This video is private.')
        return redirect('core:home')
    
    elif video.visibility == 'followers' and not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Login required'}, status=403)
        messages.error(request, 'You need to login to view this video.')
        return redirect('users:login')
    
    elif video.visibility == 'followers' and video.user != request.user and not video.user.followers.filter(id=request.user.id).exists():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Followers only'}, status=403)
        messages.error(request, 'This video is only available to followers.')
        return redirect('core:home')
    
    # Record view
    if request.user.is_authenticated:
        viewer = request.user
    else:
        viewer = None
    
    # Check if view already exists for authenticated users to prevent duplicate counts
    if viewer:
        view, created = View.objects.get_or_create(user=viewer, video=video)
    else:
        # For anonymous users, just create a new view
        View.objects.create(user=viewer, video=video)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'view_count': video.views.count(),
        })
    
    return redirect('videos:watch', video_id=video_id)

@login_required
def toggle_like_ajax(request, video_id):
    """AJAX endpoint for like/dislike toggling"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        video = get_object_or_404(Video, id=video_id)
        action = request.POST.get('action', 'like')
        
        like, created = Like.objects.get_or_create(
            user=request.user,
            video=video
        )
        
        if action == 'like':
            if not created and like.is_like:
                like.delete()
                status = 'unliked'
            else:
                like.is_like = True
                like.save()
                status = 'liked'
        elif action == 'dislike':
            if not created and not like.is_like:
                like.delete()
                status = 'undisliked'
            else:
                like.is_like = False
                like.save()
                status = 'disliked'
        
        return JsonResponse({
            'status': 'success',
            'action': status,
            'like_count': video.like_count,
            'user_like_status': 'liked' if Like.objects.filter(user=request.user, video=video, is_like=True).exists() else 'disliked' if Like.objects.filter(user=request.user, video=video, is_like=False).exists() else 'none'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)