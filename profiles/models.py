from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model): # with models.Models id will be created automatically, it can be accessed
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_ioycbx'
    )  # images is forlder name with /!! provide a default from cloudunary picture namename

    class Meta:
        ordering = ['-created_at']  # most recent first

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


# will use a create_profile function that runs specigying the User model that will send the signal
post_save.connect(create_profile, sender=User)
