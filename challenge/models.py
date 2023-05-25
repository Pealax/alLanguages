from django.db import models
from alLanguages.settings import AUTH_USER_MODEL


class Challenge(models.Model):
    state_choices = (
        ('Proceed', 'proceed'),
        ('Complete', 'complete'),
        ('Fail', 'fail'),
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    temperature = models.DecimalField(decimal_places=6, max_digits=8, default=0)
    bet = models.DecimalField(decimal_places=2, max_digits=8, null=False)
    bonus = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    state = models.CharField(max_length=8, choices=state_choices, default='Active')
    duration = models.IntegerField(null=False)
    start = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    limit = models.PositiveIntegerField()
    remainder =  models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.state