#from django.db.models import F
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
#from rest_framework.views import APIView
#from rest_framework.decorators import api_view
#from rest_framework import status

from word.models import *
from word.serializers import *


class ProgressList (ListAPIView):

    serializer_class = ProgressSerializer

    def get_queryset(self):
        user = self.request.user
        return Progress.objects.filter(user_id=user.id, translate__language=user.learn_id)


class TranslatesList (ListAPIView):

    serializer_class = TranslateSerializer

    def get_queryset(self):
        user = self.request.user
        return WordTranslate.objects.filter(language=user.learn_id, word__user=user.id)


class WordViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'put', 'head']

    queryset = Word.objects.all()
    serializer = WordSerializer

    def list(self, request, *args):
        ids = WordTranslate.objects.filter(language_id=self.request.user.learn_id,
                active=True, word__word=None).values_list('word_id', flat=True)
        queries = self.queryset.filter(id__in=ids, active=True)
        #Это выдает список всех Категорий (word_id=NULL). на learn языке. 
        #Юзер выбирает категорию=pk и его перекидывает на word/pk т.е. на retrieve
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args):
        ids = WordTranslate.objects.filter(language_id=self.request.user.learn_id,
                active=True, word__word=pk).values_list('word_id', flat=True)
        queries = self.queryset.filter(id__in=ids, active=True) #.exclude(user_id=user_id)
        #Объекты Translate, при этом КатегорияWord=pk. на языке learn.
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user=self.request.user
        word_ids = request.data['ids'] # С фронта {'ids':[list]}
        translate_ids = [translate.id 
                        for translate 
                        in WordTranslate.objects.filter(language=user.learn_id,
                                                        word_id__in=word_ids)]
        for translate_id in translate_ids:
            progress, sign = Progress.objects.get_or_create(user_id=user.id,
                                                      translate_id=translate_id)
            # Взяли или создали Прогрессы соответствующие word.id пришедших с Фронта
            progress.round += 1 # добавили 1 round
            if progress.round == 10:
                progress.is_know = True # Если раудов 10, Прогресс="знаю"
            progress.save()
        return Response()

    def create(self, request, *args):
        data = request.data
        data['user'] = request.user.id
        serializer = self.serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save() #Создание Word Юзером.
        return Response(serializer.data)

    '''
    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    '''

    '''
        word_and_progr = []
        #Массив для (Progress.round и id_Word)
        for translate in translate_obj:
            if not translate.progress_set.filter(user_id=user.id):
                word_and_progr.append((0, translate.word_id))
                # Прогресса нет, ставим round=0
            elif not translate.progress_set.filter(is_know=False):
                pass
                # Прогресс is_know, ничего не добавляем
            else:
                progress = translate.progress_set.latest('updated')
                word_and_progr.append((progress.round, translate.word_id))
                # Добавлем id_Word и соответствующий Progress.round
        slices = sorted(word_and_progr)[:20] # 20 кортежей у которых round - min.
        select = [slice[1] for slice in slices] # 20 Word_id
        queries = self.queryset.filter(id__in=select).order_by('?')[:4]
        # Из 20-ти Слов случайно выбираем 4 для изучения.
        '''

#@staticmethod
#def word_ids(lang_ids, category): #Выбор Word Категории=category, у которых есть Translate на обоих языках
#    ids1 = WordTranslate.objects.filter(language_id=lang_ids[0], active=True,
#                word__word=category).values_list('word_id', flat=True)
#    ids2 = WordTranslate.objects.filter(language_id=lang_ids[1], active=True,
#                word__word=category).values_list('word_id', flat=True)
#    word_ids = set(ids1)
#    word_ids.intersection_update(ids2)
#    return list(word_ids)