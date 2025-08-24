from django import forms
from .models import Video, Tag
import os
from django.utils.text import slugify
class VideoUploadForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        help_text='Enter tags separated by commas'
    )
    
    class Meta:
        model = Video
        fields = ['video_file', 'thumbnail', 'title', 'description', 'visibility']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            # Check file extension
            ext = os.path.splitext(video_file.name)[1].lower()
            valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm']
            if ext not in valid_extensions:
                raise forms.ValidationError('Unsupported file format. Please upload a video file.')
            
            # Check file size (100MB limit)
            if video_file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds 100MB limit.')
        
        return video_file
    
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            # Check file extension
            ext = os.path.splitext(thumbnail.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if ext not in valid_extensions:
                raise forms.ValidationError('Unsupported image format. Please upload a JPG, PNG, or GIF.')
            
            # Check file size (5MB limit)
            if thumbnail.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Thumbnail size exceeds 5MB limit.')
        
        return thumbnail
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        # Limit number of tags
        if len(tag_list) > 10:
            raise forms.ValidationError('Maximum 10 tags allowed.')
        
        # Get or create tags
        tag_objects = []
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            tag_objects.append(tag)
        
        return tag_objects
