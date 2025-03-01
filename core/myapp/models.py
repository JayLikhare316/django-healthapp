from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class usermessages(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    messagefromuser=models.TextField()
    messagefromCHatGpt=models.TextField()


class dietplan(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    dietplan=RichTextField()