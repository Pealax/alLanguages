from django.db import models
from my_user.models import User
from language.models import Language


class Question(models.Model):

    question = models.CharField(max_length=200)
    status_choices = (
        ('PR', 'Processing'),
        ('AP', 'Accepted'),
        ('RJ', 'Rejected'),
    )
    status = models.CharField(max_length=2, choices=status_choices, default='PR')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    native = models.ForeignKey(Language, related_name='lang_native',
                              on_delete=models.DO_NOTHING)
    learn = models.ForeignKey(Language, related_name='lang_learn',
                              on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.question


class Answer(models.Model):

    answer = models.CharField(max_length=50)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.answer + ', ' + str(self.correct)


class Check(models.Model):

    flag = models.BooleanField()
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment