from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Function for dynamic profile picture path (for Azure Blob Storage)
def profile_pic_upload_path(instance, filename):
    # Ensure it uses the same container for videos and profile pictures
    return f'videos/profile_pics/{instance.id}/{filename}'

class CustomUser(AbstractUser):
    # User types
    class UserType(models.TextChoices):
        CONSUMER = 'consumer', _('Consumer')
        CREATOR = 'creator', _('Creator')
        ADMIN = 'admin', _('Admin')
    
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CONSUMER,
        db_index=True  # Adding an index for faster query performance
    )
    profile_pic = models.ImageField(upload_to=profile_pic_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()
