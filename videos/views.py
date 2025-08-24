from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video, Tag
from .forms import VideoUploadForm
from interactions.models import Like, View
from django.db.models import Q
from django.db.models import Count

@login_required
def upload_video(request):
    """
    Handle video upload form submission, saving video to Azure Blob Storage.
    """
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the video object without committing it to the database yet
                video = form.save(commit=False)
                video.user = request.user  # Set the current user as the video's owner
                video.save()  # Save the video record
                form.save_m2m()  # Save many-to-many data (tags)
                
                # Display success message
                messages.success(request, 'Video uploaded successfully!')
                
                # Redirect to the watch video page
                return redirect('videos:watch', video_id=video.id)
            except Exception as e:
                # In case of an error (e.g., storage issue), display error message
                messages.error(request, f"An error occurred while uploading the video: {str(e)}")
                return redirect('videos:upload')  # Redirect back to the upload page on error
    else:
        form = VideoUploadForm()
    
    return render(request, 'videos/upload.html', {'form': form})

def watch_video(request, video_id):
    """
    View to watch a video, ensuring access control based on visibility settings.
    """
    video = get_object_or_404(Video, id=video_id)

    # Check visibility restrictions
    if video.visibility == 'private' and video.user != request.user:
        messages.error(request, 'This video is private.')
        return redirect('home')
    elif video.visibility == 'followers' and not request.user.is_authenticated:
        messages.error(request, 'You need to login to view this video.')
        return redirect('login')
    elif video.visibility == 'followers' and video.user != request.user and not video.user.followers.filter(id=request.user.id).exists():
        messages.error(request, 'This video is only available to followers.')
        return redirect('home')

    # Record view (if the user is authenticated, store their view, otherwise, leave it anonymous)
    viewer = request.user if request.user.is_authenticated else None
    View.objects.create(user=viewer, video=video)

    # Get comments, sorting by most recent first
    comments = video.comments.filter(parent=None).order_by('-created_at')

    # Check if the user liked the video
    user_like = None
    if request.user.is_authenticated:
        user_like = video.likes.filter(user=request.user).first()

    # Get related videos (most recent from the same user, excluding the current video)
    related_videos = video.user.videos.exclude(id=video.id).order_by('-created_at')[:5]

    # Get recommended videos (public, excluding current video)
    recommended_videos = Video.objects.filter(visibility='public').exclude(id=video.id).exclude(user=video.user).order_by('-created_at')[:5]

    # If not enough recommended videos, include more from the same user
    if len(recommended_videos) < 3:
        additional_videos = Video.objects.filter(visibility='public').exclude(id=video.id).order_by('-created_at')[:5 - len(recommended_videos)]
        recommended_videos = list(recommended_videos) + list(additional_videos)

    context = {
        'video': video,
        'comments': comments,
        'user_like': user_like,
        'related_videos': related_videos,
        'recommended_videos': recommended_videos,
    }

    return render(request, 'videos/watch.html', context)

@login_required
def edit_video(request, video_id):
    """
    Edit an existing video uploaded by the logged-in user.
    """
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully!')
            return redirect('videos:watch', video_id=video.id)
    else:
        form = VideoUploadForm(instance=video)
    
    return render(request, 'videos/edit.html', {'form': form, 'video': video})

@login_required
def delete_video(request, video_id):
    """
    Delete a video uploaded by the logged-in user.
    """
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('profile', username=request.user.username)
    
    return render(request, 'videos/delete.html', {'video': video})

def search(request):
    """
    Search for videos based on query (title, description, tags, or user).
    """
    query = request.GET.get('q', '')
    videos = Video.objects.filter(visibility='public')

    if query:
        videos = videos.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(user__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')
    
    context = {
        'videos': videos,
        'query': query,
    }

    return render(request, 'videos/search.html', context)

def videos_by_tag(request, tag_slug):
    """
    Display videos filtered by a specific tag.
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    videos = tag.videos.filter(visibility='public').order_by('-created_at')

    context = {
        'tag': tag,
        'videos': videos,
    }

    return render(request, 'videos/tag.html', context)
