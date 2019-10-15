from django.db import models

from django.db import models


class Video(models.Model):
    video_path = models.CharField(max_length=200)

