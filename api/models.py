from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime


def profile_images(instance, filename):
    ext = filename.split('.')[-1]
    return f'profile_images/{instance.user.username}_{datetime.now()}.{ext}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to=profile_images, default='default_profile.svg')#rename profile image before saving
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)  # Add following field
    liked_posts = models.ManyToManyField('Post', related_name='liked_by', blank=True)  # Add liked_posts field
    posts = models.ManyToManyField('Post', related_name='posted_by', blank=True)  # Add posts field


    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    # MEDIA_CHOICES = (
    #     ('image', 'Image'),
    #     ('video', 'Video'),
    # )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='post_media')
    caption = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)

    def __str__(self):
        return self.caption[:30]

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)

    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()
    
    def number_of_likes(self):
        return self.likes.count()

    def add_comment(self, user, text):
        comment = Comment.objects.create(parentPost=self, user=user, text=text)
        self.comments.add(comment)
        return comment

class Comment(models.Model):
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]
