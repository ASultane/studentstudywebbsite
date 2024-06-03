from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name= 'notes'
        verbose_name_plural='notes'

class Card(models.Model):
    id=models.AutoField
    image=models.ImageField(upload_to='media/images/')
    desc=models.CharField(max_length=80)
    title=models.CharField(max_length=40)
    cat=models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    is_finished=models.BooleanField(default=False)
    def __str__(self):
        return self.title
















