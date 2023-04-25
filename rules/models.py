from django.db import models
from my_user.models import User
from language.models import Language

class Rule(models.Model):
    rule = models.CharField(max_length=200)
    status = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nativ = models.ForeignKey(
        Language, related_name='lang_native', on_delete=models.DO_NOTHING
    )
    learn = models.ForeignKey(
        Language, related_name='lang_learn', on_delete=models.DO_NOTHING
    )
    def __str__(self):
        return self.rule

class Answer(models.Model):
    answer = models.CharField(max_length=50)
    rule = models.ForeignKey(Rule, related_name='answers', on_delete = models.CASCADE)
    def __str__(self):
        return self.answer

class Verif(models.Model):
    flag = models.BooleanField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rule = models.ForeignKey(Rule, on_delete = models.CASCADE)
    def __str__(self):
        return self.comment