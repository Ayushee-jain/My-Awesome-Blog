from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # if user account is deleted then also delete his profile
    image=models.ImageField(default='default.png',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kawrgs):
        super().save(*args,**kawrgs)  #super() -> parent class

        img=Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size) #  modifies the image to contain a thumbnail version of itself, no larger than the given size
            img.save(self.image.path)


