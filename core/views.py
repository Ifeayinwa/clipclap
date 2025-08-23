from django.shortcuts import render
from videos.models import Video
from interactions.models import View
from django.core.paginator import Paginator

def home(request):
    videos = Video.objects.filter(visibility='public').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(videos, 10)  # Show 10 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'core/home.html', context)
