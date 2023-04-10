from django.db import models
from my_user.models import User

class Rules(models.Model):
    rules = models.CharField(max_length=200)
    status = models.PositiveSmallIntegerField(default=0)
    userr = models.ForeignKey(User,  on_delete=models.DO_NOTHING)

class Answer(models.Model):
    ans = models.CharField(max_length=50)
    nr = models.ForeignKey(Rules, on_delete = models.CASCADE)

class Verif(models.Model):
    flag = models.BooleanField()
    comment = models.CharField(max_length=200)
    userv = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rules = models.ForeignKey(Rules, on_delete = models.CASCADE)