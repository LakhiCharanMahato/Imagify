# from turtle import title
from django.db import models

# Create your models here.
class Ladder(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    file=models.FileField(upload_to='')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
