
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from accounts.models import User
# User = get_user_model()

# POST MANAGER
class PostManager(models.Manager):
  def get_posts(self, *args, **kwargs):
    return self.all()

  def get_post(self, post_id, *args, **kwargs):
    return get_object_or_404(self, id=post_id)

  def get_user_posts(self, owner, *args, **kwargs):
    return self.filter(owner=owner)

  def get_user_post(self, post_id, user, *args, **kwargs):
    return get_object_or_404(self, pk=post_id, owner=user)


# POST MODEL
class Post(models.Model):
  # title = models.CharField(max_length=100)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  # owner = models.ForeignKey(
  #   User,
  #   default=1,
  #   on_delete=models.CASCADE,
  #   null=True
  # )
  owner_id = models.CharField(null=False,max_length=10,default=1)
  image = models.ImageField(upload_to='images/',null=True)
  active = models.BooleanField(default=True)
  privacy = models.BooleanField(default=True)


  objects = PostManager()

  def __str__(self, *args, **kwargs):
    return self.owner_id

  def get_absolute_url(self, *args, **kwargs):
    return reverse('posts:posts-detail', kwargs={'id': self.pk})
  
  def get_delete_url(self, *args, **kwargs):
    return reverse('posts:posts-delete', kwargs={'id': self.pk})

  def get_update_url(self, *args, **kwargs):
    return reverse('posts:posts-update', kwargs={'id': self.pk})

  def get_like_url(self, *args, **kwargs):
    return reverse('likes:post-likes', kwargs={'id': self.pk})