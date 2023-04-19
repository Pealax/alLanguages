from rest_framework import serializers
from .models import *

class VerifSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=False)
    class Meta:
        model = Verif
        fields = ['id','flag','comment','rules','date']
    def create(self, validated_data):
        instance = Verif.objects.create(**validated_data)
        return instance

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['ans']

class RulesSerializer(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True, required=False)
    class Meta:
        model = Rules
        fields = ['id', 'rules', 'status','answers']

class RulesAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Rules
        fields = ['id','rules','answers']
    def create(self, validated_data):
        answers = validated_data.pop('answers')
        instance = Rules.objects.create(**validated_data)
        for ans in answers:
            Answer.objects.create(nr=instance, **ans)
        return instance
    def update(self, instance, validated_data):
        instance.rules = validated_data.get('rules')
        instance.status = 0
        instance.save()
        answupd = validated_data.get('answers')
        answers = Answer.objects.filter(nr = instance)
        k=0
        for answ in answers:
            answ.ans = answupd[k].get('ans')
            k+=1
        answers.bulk_update(answers, ['ans'])
        return instance

class RulesVerifySerializer(serializers.ModelSerializer):
    rules = serializers.StringRelatedField(required=False, allow_null=True,)
    answers = serializers.StringRelatedField(many=True, required=False, allow_null=False,)
    verif_set = VerifSerializer(many=True)
    class Meta:
        model = Rules
        fields = ['id','rules', 'answers','verif_set']