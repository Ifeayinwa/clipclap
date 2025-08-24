from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video, Tag
from .forms import VideoUploadForm
from interactions.models import Like, View
from django.db.models import Q
from django.db.models import Count
import traceback

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
                
                # Save tags (many-to-many relationship)
                tags = form.cleaned_data['tags']
                video.tags.set(tags)
                
                # Display success message
                messages.success(request, 'Video uploaded successfully!')
                
                # Redirect to the watch video page
                return redirect('videos:watch', video_id=video.id)
            except Exception as e:
                # Log the full error for debugging
                error_traceback = traceback.format_exc()
                print(f"Upload error: {error_traceback}")
                
                # In case of an error (e.g., storage issue), display error message
                messages.error(request, f"An error occurred while uploading the video: {str(e)}")
                return redirect('videos:upload')  # Redirect back to the upload page on error
        else:
            # Form is not valid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
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
            try:
                form.save()
                # Update tags
                tags = form.cleaned_data['tags']
                video.tags.set(tags)
                
                messages.success(request, 'Video updated successfully!')
                return redirect('videos:watch', video_id=video.id)
            except Exception as e:
                messages.error(request, f"An error occurred while updating the video: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # Pre-populate tags field
        initial_tags = ', '.join([tag.name for tag in video.tags.all()])
        form = VideoUploadForm(instance=video, initial={'tags': initial_tags})
    
    return render(request, 'videos/edit.html', {'form': form, 'video': video})

@login_required
def delete_video(request, video_id):
    """
    Delete a video uploaded by the logged-in user.
    """
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        try:
            video.delete()
            messages.success(request, 'Video deleted successfully!')
            return redirect('profile', username=request.user.username)
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the video: {str(e)}")
            return redirect('videos:watch', video_id=video.id)
    
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

# Debug views
def debug_storage(request):
    """Debug view to check storage configuration"""
    from storages.backends.azure_storage import AzureStorage
    try:
        storage = AzureStorage()
        # Try to list files to check connection
        files = storage.listdir('')
        return render(request, 'videos/debug.html', {
            'files': files,
            'account_name': storage.account_name,
            'container_name': storage.container_name,
            'connection_success': True
        })
    except Exception as e:
        return render(request, 'videos/debug.html', {
            'error': str(e),
            'connection_success': False
        })

@login_required
def test_upload(request):
    """Test view to check if upload works"""
    if request.method == 'POST':
        # Simple file upload test
        from storages.backends.azure_storage import AzureStorage
        storage = AzureStorage()
        
        test_file = request.FILES.get('test_file')
        if test_file:
            try:
                filename = f"test_{request.user.id}_{test_file.name}"
                saved_name = storage.save(filename, test_file)
                url = storage.url(saved_name)
                
                return render(request, 'videos/test_upload.html', {
                    'success': True,
                    'filename': saved_name,
                    'url': url
                })
            except Exception as e:
                return render(request, 'videos/test_upload.html', {
                    'success': False,
                    'error': str(e)
                })
    
    return render(request, 'videos/test_upload.html')
