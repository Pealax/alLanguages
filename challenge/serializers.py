import math
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import *


class ChallengeSerializer(serializers.ModelSerializer):

    temperature = serializers.DecimalField(decimal_places=6, max_digits=8, required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)

    class Meta:

        model = Challenge
        fields = ['id', 'state', 'temperature', 'bid', 'bonus', 'start', 'end']

    def create(self, validated_data):
        instance = Challenge.objects.create(**validated_data)
        #instance.end = instance.start + timedelta(days=7)
        #instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.temperature += validated_data.get('temperature')
        temperature = instance.temperature
        bid = instance.bid
        time_to_end = instance.end - datetime.now(tz=timezone.utc)
        instance.state = self.set_state(temperature, time_to_end)
        if instance.state == 'Complete':
            instance.bonus = self.calc_bonus(temperature, bid)
        instance.save()
        return instance

    @staticmethod
    def set_state(temperature, time):
        state = 'Active'
        if time.total_seconds() <= 0:
            if temperature >= 72:
                state = 'Complete'
            else:
                state = 'Fail'
        else:
            if temperature < 36:
                state = 'Fail'
        return state
            
    @staticmethod
    def calc_bonus(temperature, bid):
        coeff_bonus = 1.001**float(temperature)
        threshold = 100
        regress = 1.0
        if bid > threshold:
            regress = 1.0 - math.log10(bid/threshold)/4
        elif bid > threshold * 100:
            regress = 0.5
        bonus = bid * regress * (coeff_bonus - 1)
        return bonus