from rest_framework import serializers
from word.models import Word, WordTranslate, Progress


class TranslateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordTranslate
        fields = '__all__'


class QuerySerializer(serializers.ModelSerializer):
    translates = TranslateSerializer(source='translate_set', many=True)

    def get_translates(self, instance):
        print('HERE!!!!!!!!!!!!!!!!!!')
        return {instance.id: 123}

    class Meta:
        model = Word
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Progress
        fields = '__all__'


class WordTranslateSerializer(serializers.ModelSerializer):
    word = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    progress = ProgressSerializer(read_only=True)

    def get_progress(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user
            progress, _ = Progress.objects.get_or_create(user_id=user.id, translate_id=obj.id)

            return progress.round
        return

    class Meta:
        model = WordTranslate
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    #translates = WordTranslateSerializer(many=True, required=False)

    class Meta:
        model = Word
        exclude = ['review']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user = self.context['request'].user

        if not user.learn_id and user.native_id:
            print('IF', user.learn_id, user.native_id)

            translates = WordTranslate.objects.filter(word_id=instance.id, 
                                                      language_id__in=[user.native.id, user.learn.id])

            native = translates[0]
            learn = translates[1]
            if learn.language_id != user.learn_id:
                native, learn = learn, native

            response['native'] = native.text
            if learn.sound:
                response['sound'] = learn.sound.url
            response['learn'] = learn.text

            progress, _ = Progress.objects.get_or_create(user_id=user.id, translate_id=learn.id)
            response['progress'] = progress.round

            if 'words' in response:
                response['words'] = sorted(response['words'], key=lambda x: x['progress'])
                response['words_play'] = response['words'][0:4]
        else:
            #response['translates'] = WordTranslate.objects.filter(word_id=instance.id)
            objects = WordTranslate.objects.filter(word_id=instance.id, 
                                                   language_id__in=[user.native.id, user.learn.id])
            response['translates'] = [WordTranslateSerializer(object).data for object in objects]
        return response

    def get_fields(self):
        fields = super(WordSerializer, self).get_fields()
        fields['words'] = WordSerializer(many=True, read_only=True)
        return fields

    def create(self, validated_data):
        value = validated_data.pop('data')['value']
        #instance = Entity.objects.create(value=value, **validated_data)
        instance = Word.objects.create(value=value, **validated_data)

        return instance


'''    def update(self, pk, request):
        progress = Progress.objects.filter(user_id=request.user.id).filter(word_id__in=request.data).order_by('level')
        user_progress = progress.filter(level=progress[0].level).update(level=F('level') + 1)


        for item in remove_items.values():
            item.delete()

        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()

        return instance'''


'''
class QueryTranslateSerializer(serializers.ModelSerializer):
    query = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = QueryTranslate
        fields = '__all__'
        '''

'''def get_native(self, instance):
        user = self.context['request'].user
        translate = WordTranslate.objects.get(word_id=instance.id, language_id=user.native.id)
        return translate.text'''
'''

class QuerySerializer(serializers.ModelSerializer):
    native = serializers.SerializerMethodField()

    class Meta:
        model = Query
        fields = '__all__'

    def get_native(self, obj):
        user = self.context['request'].user
        translate = QueryTranslate.objects.get(language_id=user.native_id)
        return translate.text'''

'''
class QueryDetailSerializer(QuerySerializer):
    native = serializers.SerializerMethodField()
    words = WordSerializer(source='word_set', many=True, read_only=True)

    class Meta:
        model = Query
        fields = '__all__'

    def get_native(self, obj):
        user = self.context['request'].user
        translate = QueryTranslate.objects.get(language_id=user.native_id)
        return translate.text

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['words'] = sorted(response['words'], key=lambda x: x['progress'])
        response['words_play'] = response['words'][0:4]
        return response
'''
'''
class QueryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        instance = Query.objects.create(**validated_data)
        return instance
'''
'''
class QuerySetSerializer(serializers.ModelSerializer):
    native = serializers.SerializerMethodField(read_only=True)
    words = WordSerializer(many=True, read_only=True)
    translates = QueryTranslateSerializer(many=True, required=False)

    # images = LotImageSerializer(many=True, required=False)
    # user = UserSerializer(read_only=True)

    # free_numbers = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Query
        fields = '__all__'

    def get_native(self, instance):
        translate = QueryTranslate.objects.get(query_id=instance.id, language_id=instance.user.native_id)
        return translate.text

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if 'words' in response:
            response['words'] = sorted(response['words'], key=lambda x: x['progress'])
            response['words_play'] = response['words'][0:4]
        return response

    def create(self, validated_data):
        translates_data = validated_data.pop('translates', [])
        query = Query.objects.create(**validated_data)

        if translates_data:
            query.translates = QueryTranslate.objects.bulk_create(
                QueryTranslate(query=query, **translate)
                for translate in translates_data
            )
        return query


 user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        source='user',
        write_only=True
    ) 
    language_ids = [self.request.user.learn_id, self.request.user.native_id]
        query_ids = QueryTranslate.objects.filter(language_id__in=language_ids).values_list('query_id', flat=True)
        ids = [id_ for id_ in query_ids if list(query_ids).count(id_) > 1]

        return Query.objects.filter(id__in=list(set(ids)))


    conditions = ConditionSerializer(many=True, required=False)
    # wins = NumberSerializer(many=True, read_only=True)
        def create(self, validated_data):
        conditions_data = validated_data.pop('conditions', [])
        lot = Lot.objects.create(**validated_data)
        if conditions_data:
            Condition.objects.bulk_create(
                Condition(lot=lot, **condition)
                for condition in conditions_data
            )
        return '''




