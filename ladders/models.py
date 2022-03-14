# from turtle import title
from django.db import models
from pyffmpeg import FFmpeg

# Create your models here.
class Ladder(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    file=models.FileField(upload_to='')
    thumbnail=models.FileField(null=True,upload_to='')
    content_type=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.content_type=self.file.file.content_type
        if(self.content_type == 'video/mp4'):
            self.thumbnail=None#FFmpeg.convert(self,input_file=self.file,output_file='imaged.png')
        else:
            self.thumbnail=None
        super().save(*args,**kwargs)
