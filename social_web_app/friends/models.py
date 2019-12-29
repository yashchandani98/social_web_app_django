from django.db import models

# Create your models here.
class Friends(models.Model):
    requested_user = models.IntegerField(null=False)
    received_user = models.IntegerField(null=False)
    active = models.BooleanField(default=True)
    connected_date = models.DateTimeField(auto_now_add=True)
    # request_date = models.DateTimeField(auto_now_add=True)
class FriendRequest(models.Model):
    requested_user = models.IntegerField(null=False)
    received_user = models.IntegerField(null=False)
    active = models.BooleanField(default=True)
    request_date = models.DateTimeField(auto_now_add=True)