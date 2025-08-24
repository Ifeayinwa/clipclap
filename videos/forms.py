from django import forms
from .models import Video, Tag

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
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        # Get or create tags
        tag_objects = []
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            tag_objects.append(tag)
        
        return tag_objects
