import math
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import *


class ChallengeHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Challenge
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):

    end = serializers.DateTimeField(required=False)

    class Meta:

        model = Challenge
        fields = ['id', 'state', 'temperature', 'bet', 'start', 'update', 'duration', 'end']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['end'] = instance.start + timedelta(days=instance.duration)
        return representation

    def create(self, validated_data):
        user_id = self.context.get('request').user.id
        instance = Challenge.objects.create(**validated_data, user_id=user_id)
        return instance

class ChallengeUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Challenge
        fields = ['id', 'state', 'temperature', 'start', 'update', 'bonus']

    def update(self, instance, validated_data):
        heat = validated_data.get('temperature', 0)
        temperature = instance.temperature
        bet = instance.bet
        start = instance.start
        update = instance.update
        duration = instance.duration
        time_now = datetime.now(tz=timezone.utc)
        days_last_upd = (time_now - start).days - (update - start).days
        time_to_end = start + timedelta(days=duration) - time_now        
        temperature = self.calc_temperature(temperature, heat, days_last_upd)
        instance.state = self.set_state(temperature, time_to_end)
        if instance.state == 'Complete':
            instance.bonus = float(bet) * self.calc_bonus(temperature, duration) * self.calc_regress(bet)
        elif instance.state == 'Fail':
            instance.bonus = -bet
        instance.temperature = temperature
        instance.save()
        return instance

    @staticmethod
    def calc_temperature(temperature, heat, days):
        scale = 50
        cool = 3
        return temperature + heat/(1+temperature/scale) - days*cool

    @staticmethod
    def set_state(temperature, time):
        frozen = 0
        if temperature >= frozen:
            if time.total_seconds() > 0:
                return 'Active'
            else:
                return 'Complete'
        else:
            return 'Fail'

    @staticmethod
    def calc_bonus(temperature, duration):
        return 1.001**float(duration) * 1.003**float(temperature) - 1

    @staticmethod
    def calc_regress(bet):
        threshold = 100
        if bet > threshold:
            regress = 1.0 - math.log10(bet/threshold)/4
        elif bet > threshold * 100:
            regress = 0.5
        return regress