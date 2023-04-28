from rest_framework import serializers
from .models import *


class CheckSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(required=False)

    class Meta:

        model = Check
        fields = ['id', 'flag', 'comment', 'question', 'date']

    def create(self, validated_data):
        instance = Check.objects.create(**validated_data)
        return instance


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Answer
        fields = ['answer']


class QuestionSerializer(serializers.ModelSerializer):

    answers = serializers.StringRelatedField(many=True, required=False)

    class Meta:

        model = Question
        fields = ['id', 'question', 'answers']


class QuestionAnswersSerializer(serializers.ModelSerializer):

    status = serializers.CharField(max_length=2, required=False)
    answers = AnswerSerializer(many=True)

    class Meta:

        model = Question
        fields = ['id', 'question', 'status', 'answers']

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        instance = Question.objects.create(**validated_data)
        answer_objs = [Answer(question=instance, **answer) for answer in answers]
        Answer.objects.bulk_create(answer_objs)
        return instance

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.status = 'PR'
        instance.save()
        answupd = validated_data.get('answers')
        answers = Answer.objects.filter(question=instance)
        for (i, answer) in enumerate(answers):
            answer.answer = answupd[i].get('answer')
        answers.bulk_update(answers, ['answer'])
        Check.objects.filter(question=instance).delete()
        return instance


class QuestionCheckSerializer(serializers.ModelSerializer):

    question = serializers.StringRelatedField(required=False)
    answers = serializers.StringRelatedField(many=True, required=False)
    check_set = CheckSerializer(many=True)

    class Meta:

        model = Question
        fields = ['id', 'question', 'answers', 'check_set']