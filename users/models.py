from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  address = models.TextField()

  phone = models.CharField(max_length=10)

  gender = models.CharField(max_length=1,choices=(('F','Femenino'),('M','Masculino')))

  def __str__(self):
    return self.user.username