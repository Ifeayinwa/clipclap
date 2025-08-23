from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def profile_pic_upload_path(instance, filename):
    # Upload to profile_pics/username/filename
    return os.path.join('profile_pics', instance.username, filename)

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
    )
    profile_pic = models.ImageField(
        upload_to=profile_pic_upload_path,
        blank=True,
        null=True,
        default='profile_pics/default.png'
    )
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='following'
    )
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    def get_profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        return '/static/images/default_profile.png'

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.profile_pic:
        # Set default profile pic if none was provided
        instance.profile_pic = 'profile_pics/default.png'
        instance.save()