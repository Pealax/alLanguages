from rest_framework import serializers
from word.models import Word, WordTranslate, Progress


class TranslateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordTranslate
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):

    translate = TranslateSerializer()

    class Meta:
        model = Progress
        fields = ['user', 'translate', 'round', 'is_know']


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        exclude = ['review']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user = self.context['request'].user
        objects = WordTranslate.objects.filter(word_id=instance.id, 
                    language_id__in=[user.native.id, user.learn.id])
        response['translates'] = [TranslateSerializer(object).data for object in objects]
        return response

    '''
    def update(self, pk, request):
        progress = Progress.objects.filter(user_id=request.user.id).filter(word_id__in=request.data).order_by('level')
        user_progress = progress.filter(level=progress[0].level).update(level=F('level') + 1)

        for item in remove_items.values():
            item.delete()

        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance 
    '''

'''
    conditions = ConditionSerializer(many=True, required=False)
    wins = NumberSerializer(many=True, read_only=True)
        def create(self, validated_data):
        conditions_data = validated_data.pop('conditions', [])
        lot = Lot.objects.create(**validated_data)
        if conditions_data:
            Condition.objects.bulk_create(
                Condition(lot=lot, **condition)
                for condition in conditions_data
            )
        return 
'''