
from unittest.util import _MAX_LENGTH
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime

User=get_user_model()

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id_user=models.IntegerField()
    bio=models.TextField(blank=True)
    profileimg=models.ImageField(upload_to='profile_images',default='batman.jpg')
    location=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return (self.user.username) # type: ignore

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField('post_images',upload_to='uploaded_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def __str__(self):
        return self.user

class LikePost(models.Model):
 post_id=models.CharField(max_length=500)
 username=models.CharField(max_length=500)

 def __str__(self):
     return self.username
 
class follow(models.Model):
  follower=models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
  followed=models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)
  created_at=models.DateTimeField(default=datetime.now)

  class Meta:
     unique_together=('follower','followed')
      