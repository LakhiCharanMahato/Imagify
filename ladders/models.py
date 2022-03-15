# from turtle import title
from django.db import models
# from pyffmpeg import FFmpeg
from django.contrib.auth.models import User

# Create your models here.
class Ladder(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    file=models.FileField(upload_to='')
    thumbnail=models.FileField(null=True,upload_to='')
    content_type=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    user_name=models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    # user_name=models.TextField()


    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if self.content_type:
            pass
        else:
            self.content_type=self.file.file.content_type
        # self.user_name=username
        if(self.content_type == 'video/mp4'):
            self.thumbnail=None#FFmpeg.convert(self,input_file=self.file,output_file='imaged.png')
        else:
            self.thumbnail=None
        super().save(*args,**kwargs)

    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)
