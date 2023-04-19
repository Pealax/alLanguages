from django.db import models
from my_user.models import User
from language.models import Language

class Rules(models.Model):
    rules = models.CharField(max_length=200)
    status = models.PositiveSmallIntegerField(default=0)
    userr = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    langnativ = models.ForeignKey(Language, related_name='langnative', on_delete=models.DO_NOTHING)
    langlearn = models.ForeignKey(Language, related_name='langlearn', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.rules

class Answer(models.Model):
    ans = models.CharField(max_length=50)
    nr = models.ForeignKey(Rules, related_name='answers', on_delete = models.CASCADE)
    def __str__(self):
        return self.ans

class Verif(models.Model):
    flag = models.BooleanField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add = True)
    userv = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rules = models.ForeignKey(Rules, on_delete = models.CASCADE)
    def __str__(self):
        return self.comment