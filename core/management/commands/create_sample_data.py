from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from videos.models import Video, Tag
from interactions.models import Like, Comment, View
import random
from faker import Faker
import os
from django.core.files import File

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Creates sample data for testing and development'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        users = []
        for i in range(10):
            user_type = 'creator' if i < 5 else 'consumer'
            user = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password='testpass123',
                user_type=user_type,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(),
                website=fake.url()
            )
            
            # Add a profile picture (using a placeholder)
            profile_pic_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'images', 'profile_pic.png')
            if os.path.exists(profile_pic_path):
                with open(profile_pic_path, 'rb') as f:
                    user.profile_pic.save(f'profile_{user.username}.png', File(f))
            
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')
        
        # Create some followers
        for user in users:
            if user.user_type == 'creator':
                for follower in random.sample(users, random.randint(1, 5)):
                    if follower != user:
                        user.followers.add(follower)
        
        # Create some tags
        tags = []
        for tag_name in ['funny', 'music', 'dance', 'tutorial', 'gaming', 'food', 'travel', 'fitness', 'art', 'fashion']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            self.stdout.write(f'Created tag: {tag.name}')
        
        # Create sample videos (only by creators)
        creators = [user for user in users if user.user_type == 'creator']
        video_files = ['sample1.mp4', 'sample2.mp4', 'sample3.mp4']  # These should be in your media/videos folder
        
        for i in range(20):
            creator = random.choice(creators)
            video = Video.objects.create(
                user=creator,
                title=fake.sentence(),
                description=fake.text(),
                visibility=random.choice(['public', 'public', 'public', 'followers', 'private'])
            )
            
            # Add a video file (using a placeholder)
            video_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'media', 'videos', random.choice(video_files))
            if os.path.exists(video_file_path):
                with open(video_file_path, 'rb') as f:
                    video.video_file.save(f'video_{video.id}.mp4', File(f))
            
            # Add a thumbnail (using a placeholder)
            thumbnail_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'images', 'thumbnail.png')
            if os.path.exists(thumbnail_path):
                with open(thumbnail_path, 'rb') as f:
                    video.thumbnail.save(f'thumbnail_{video.id}.png', File(f))
            
            # Add some tags
            video.tags.set(random.sample(tags, random.randint(1, 3)))
            
            self.stdout.write(f'Created video: {video.title}')
        
        # Create likes, comments, and views
        videos = Video.objects.all()
        for video in videos:
            # Views
            for i in range(random.randint(0, 100)):
                viewer = random.choice(users) if random.random() > 0.3 else None
                View.objects.create(video=video, user=viewer)
            
            # Likes
            likers = random.sample(users, random.randint(0, len(users)))
            for liker in likers:
                Like.objects.create(user=liker, video=video, is_like=True)
            
            # Comments
            for i in range(random.randint(0, 10)):
                commenter = random.choice(users)
                comment = Comment.objects.create(
                    user=commenter,
                    video=video,
                    text=fake.sentence()
                )
                
                # Some replies to comments
                if random.random() > 0.7:
                    for j in range(random.randint(0, 3)):
                        replier = random.choice(users)
                        Comment.objects.create(
                            user=replier,
                            video=video,
                            text=fake.sentence(),
                            parent=comment
                        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))
