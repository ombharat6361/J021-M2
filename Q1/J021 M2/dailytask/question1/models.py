from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    description=models.TextField(null=True, blank=True)
    complete=models.BooleanField()
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name