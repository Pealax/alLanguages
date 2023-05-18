from django.db import models
from my_user.models import User


'''class Condition(models.Model):
    type = models.CharField(max_length=20)
    coeff = models.DecimalField(decimal_places=8, max_digits=6)'''


class Challenge(models.Model):
    state_choices = (
        ('Active', 'active'),
        ('Complete', 'complete'),
        ('Fail', 'fail'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    #last_upd = models.DateTimeField(auto_now=True)
    temperature = models.DecimalField(decimal_places=6, max_digits=8, default=50)
    bid = models.IntegerField(default=10)
    bonus = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    state = models.CharField(max_length=8, choices=state_choices, default='Active') 

    def __str__(self):
        return self.state