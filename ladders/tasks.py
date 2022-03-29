from __future__ import absolute_import, unicode_literals

from celery import shared_task
import subprocess
import os

@shared_task(bind=True)
def easy_thumbnail(self,content_type,file_url,id): 
    if(content_type == 'video/mp4'):
        # self.thumbnail=None
        # ff=FFmpeg()
        # print(self.file.url)
        # print(self.id)
        
        # self.thumbnail=ff.convert(input_file=self.file,output_file='/media/imaged.png')
        video_input_path="static/"+file_url
        image_output_path='static/media/imaged'+f'{id}'+'.png'
        subprocess.call(['ffmpeg', '-i',video_input_path, '-ss', '00:00:01.000', '-vframes', '1', image_output_path])
        # thumbnail='/media/imaged'+f'{id}'+'.png'
    # else:
        # thumbnail=None        
    # super().save(*args,**kwargs)
