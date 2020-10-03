from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'


class Student(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    sex = models.BooleanField(default=True)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Student'
