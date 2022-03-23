# from turtle import title
from django.db import models
# from pyffmpeg import FFmpeg
# from django.contrib.auth.models import User
from django.conf import settings


import subprocess
import os

# Create your models here.
class Ladder(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    file=models.FileField(upload_to='')
    # thumbnail=models.FileField(null=True,upload_to='')
    thumbnail=models.TextField(null=True)
    content_type=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    user_name=models.ForeignKey(settings.AUTH_USER_MODEL,default=None,on_delete=models.CASCADE)
    # user_name=models.TextField()


    def __str__(self):
        return self.title

    def get_thumbnail(self):
        return self.thumbnail.__str__()

    def save(self,*args,**kwargs):
        if self.content_type:
            pass
        else:
            self.content_type=self.file.file.content_type
        # self.user_name=username

        # if(self.content_type == 'video/mp4'):
        #     # self.thumbnail=None
        #     # ff=FFmpeg()
        #     print(self.file.url)
        #     print(self.id)

        #     # self.thumbnail=ff.convert(input_file=self.file,output_file='/media/imaged.png')
        #     video_input_path="static/"+self.file.url
        #     image_output_path='static/media/imaged'+'{{self.id}}'+'.png'
        #     self.thumbnail=subprocess.call(['ffmpeg', '-i',video_input_path, '-ss', '00:00:01.000', '-vframes', '1', image_output_path])
        # else:
        #     self.thumbnail=None
        self.thumbnail=None
        super().save(*args,**kwargs)
        if(self.content_type == 'video/mp4'):
            # self.thumbnail=None
            # ff=FFmpeg()
            print(self.file.url)
            print(self.id)
            
            # self.thumbnail=ff.convert(input_file=self.file,output_file='/media/imaged.png')
            video_input_path="static/"+self.file.url
            image_output_path='static/media/imaged'+f'{self.id}'+'.png'
            subprocess.call(['ffmpeg', '-i',video_input_path, '-ss', '00:00:01.000', '-vframes', '1', image_output_path])
            self.thumbnail='/media/imaged'+f'{self.id}'+'.png'
        else:
            self.thumbnail=None        
        super().save(*args,**kwargs)

      

    def delete_thumbnail(self,*args,**kwargs):
        if self.get_thumbnail():
            fname='static'+ self.get_thumbnail()
            if os.path.exists(fname):
                os.remove(fname)
                print("Success")
    
    def delete(self,*args,**kwargs):
        self.delete_thumbnail()
        try:
            if self.file:
                self.file.delete()
            super().delete(*args,**kwargs)
        except:
            pass
