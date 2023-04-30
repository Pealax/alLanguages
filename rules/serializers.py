from django.db.models import Sum
from rest_framework import serializers
from .models import *


class CheckSerializer(serializers.ModelSerializer):

    class Meta:

        model = Check
        fields = ['id', 'flag', 'comment', 'question']

    def create(self, validated_data):
        instance = Check.objects.create(**validated_data)
        question_id = instance.question_id
        checks_question = Check.objects.filter(question_id=question_id)
        count = checks_question.count()
        sum = checks_question.aggregate(Sum('flag'))['flag__sum']
        if count - sum >= 3:
            self.set_status(question_id, 'RJ')
        elif 2*sum - count >= 3:
            self.set_status(question_id, 'AP')
        return instance
    
    @staticmethod
    def set_status(question_id, status):
        question = Question.objects.get(id=question_id)
        question.status = status
        question.save()


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Answer
        fields = ['answer', 'correct']


class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

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
        user = validated_data['user']
        answers = validated_data.pop('answers')
        instance = Question.objects.create(**validated_data,
                    user_id=user.id,
                    native_id=user.native_id,
                    learn_id=user.learn_id)
        answer_objs = [Answer(question=instance, **answer) for answer in answers]
        Answer.objects.bulk_create(answer_objs)
        return instance

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.status = 'PR'
        instance.save()
        Check.objects.filter(question=instance).delete()
        Answer.objects.filter(question=instance).delete()
        answers = validated_data.pop('answers')
        answer_objs = [Answer(question=instance, **answer) for answer in answers]
        Answer.objects.bulk_create(answer_objs)
        return instance


class QuestionCheckSerializer(serializers.ModelSerializer):

    question = serializers.StringRelatedField(required=False)
    answers = serializers.StringRelatedField(many=True, required=False)
    check_set = CheckSerializer(many=True)

    class Meta:

        model = Question
        fields = ['id', 'question', 'answers', 'check_set']