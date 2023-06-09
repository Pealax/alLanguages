from django.db import models
from alLanguages.settings import AUTH_USER_MODEL
from language.models import Language


class Category(models.Model):

    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class CategoryTranslate(models.Model):

    text = models.CharField(max_length=50)
    native = models.ForeignKey(Language, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.text


class Question(models.Model):

    question = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    # При удалении Категории, наверно, не надо удалять все Вопросы ?
    status_choices = (
        ('Proceed', 'proceed'),
        ('Complete', 'complete'),
        ('Reject', 'reject'),
    )
    status = models.CharField(max_length=8, choices=status_choices, default='Proceed')
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
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
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment