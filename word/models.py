from django.db import models
from alLanguages.settings import AUTH_USER_MODEL
from language.models import Language


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.active)

    class Meta:
        abstract = True


class Word(BaseModel):
    word = models.ForeignKey('self', related_name='word_set', 
                             on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, null=True, blank=True)
    level = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='word/image/', null=True)
    review = models.PositiveIntegerField(default=0)


class WordTranslate(BaseModel):
    word = models.ForeignKey(Word, related_name='translate_set', 
                             on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='language_set', 
                                 on_delete=models.CASCADE)
    text = models.CharField(max_length=32)
    transcription = models.CharField(max_length=32, null=True)
    sound = models.FileField(upload_to='word/sound/', null=True)

    def __str__(self):
        return self.text


class Progress(BaseModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    translate = models.ForeignKey(WordTranslate, on_delete=models.CASCADE)
    round = models.PositiveSmallIntegerField(default=0)
    is_know = models.BooleanField(default=False)
    active = None

    def __str__(self):
        return 'Translate: ' + str(self.translate) + 'Round: ' + str(self.round)