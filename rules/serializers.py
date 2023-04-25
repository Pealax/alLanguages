from rest_framework import serializers
from .models import *

class VerifSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=False)

    class Meta:
        model = Verif
        fields = ['id','flag','comment','rule','date']

    def create(self, validated_data):
        instance = Verif.objects.create(**validated_data)
        return instance

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer']

class RulesSerializer(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Rule
        fields = ['id', 'rule', 'status','answers']

class RulesAnswerSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(default=0, required=False)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Rule
        fields = ['id', 'rule', 'status', 'answers']

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        instance = Rule.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(rule=instance, **answer)
        return instance

    def update(self, instance, validated_data):
        instance.rule = validated_data.get('rule')
        instance.status = 0
        instance.save()
        answupd = validated_data.get('answers')
        answers = Answer.objects.filter(rule=instance)
        k=0
        for answer in answers:
            answer.answer = answupd[k].get('answer')
            k+=1
        answers.bulk_update(answers, ['answer'])
        Verif.objects.filter(rule=instance).delete()
        return instance

class RulesVerifySerializer(serializers.ModelSerializer):
    rule = serializers.StringRelatedField(required=False)
    answers = serializers.StringRelatedField(many=True, required=False)
    verif_set = VerifSerializer(many=True)

    class Meta:
        model = Rule
        fields = ['id', 'rule', 'answers', 'verif_set']