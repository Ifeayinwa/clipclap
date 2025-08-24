from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid
from storages.backends.azure_storage import AzureStorage
from django.core.exceptions import ValidationError
import os

User = get_user_model()

def validate_video_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.webm']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file format. Please upload a video file.')

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(
        upload_to='videos/%Y/%m/%d/', 
        storage=AzureStorage(),
        validators=[validate_video_file_extension]
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        storage=AzureStorage()
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='videos')
    visibility = models.CharField(
        max_length=10,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('followers', 'Followers Only'),
        ],
        default='public'
    )

    def __str__(self):
        return f'{self.title} by {self.user.username}'

    @property
    def like_count(self):
        return self.likes.filter(is_like=True).count()

    @property
    def comment_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
