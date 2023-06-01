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
        #Это выдает список всех категорий (word_id=NULL). на learn языке. 
        #Юзер выбирает категорию=pk и его перекидывает на word/pk т.е. на retrieve
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args):
        user = self.request.user
        translate_obj = WordTranslate.objects.filter(language_id=user.learn_id,
                active=True, word__word=pk)
        #Объекты Translate, при этом КатегорияWord=pk. на языке learn. 
        #.exclude(word__user=user_id) Убрать Word созданные самим Юзером?
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
        slice = sorted(word_and_progr)[:20] # 20 кортежей у которых round - min.
        select = [slice[1] for slice in slice] # 20 Word_id
        queries = self.queryset.filter(id__in=select).order_by('?')[:4]
        # Из 20-ти Слов случайно выбираем 4 для изучения.
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user=self.request.user
        word_ids = request.data['ids'] # С фронта {'id':[list]}
        translate_ids = [translate.id 
                        for translate 
                        in WordTranslate.objects.filter(language=user.learn_id,
                                                        word_id__in=word_ids)]
        for translate_id in translate_ids:
            progress, sign = Progress.objects.get_or_create(user_id=user.id,
                                                      translate_id=translate_id)
            # Взяли или создали Прогрессы соответствующие word.id пришедших с Фронта
            progress.round += 1
            # добавили 1 round
            if progress.round == 10:
                progress.is_know = True
            # Если раудов 10, Прогресс="знаю"
            progress.save()
        return Response()

    def create(self, request, *args):
        data = request.data
        data['user'] = request.user.id
        serializer = self.serializer(data=data, context={'request': request})
        serializer.is_valid()
        serializer.save() #Создание Word Юзером.
        return Response(serializer.data)

#@staticmethod
#def word_ids(lang_ids, category): #Выбор Word Категории=category, у которых есть Translate на обоих языках
#    ids1 = WordTranslate.objects.filter(language_id=lang_ids[0], active=True,
#                word__word=category).values_list('word_id', flat=True)
#    ids2 = WordTranslate.objects.filter(language_id=lang_ids[1], active=True,
#                word__word=category).values_list('word_id', flat=True)
#    word_ids = set(ids1)
#    word_ids.intersection_update(ids2)
#    return list(word_ids)
    

    '''
    def update(self, request, pk=None):
        query_progress = Progress.objects.filter(user_id=request.user.id).filter(translate__word_id=pk)
        word_ids = [word_id for word_id in request.data]
        current_progress = query_progress.filter(translate_id__in=word_ids).order_by('round')

        if len(current_progress):
            updated_progress = current_progress.filter(round=current_progress[0].round).update(round=F('round') + 1)
            low_progress = query_progress.exists(round=current_progress[0].round + 1)
            if low_progress - updated_progress == 0:
                translate = WordTranslate.objects.get(word_id=pk, language_id=request.user.learn_id)
                progress = Progress.objects.get(translate_id=translate.id)
                progress.round += 1
                progress.save()
        return Response()'''

    '''
    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''
    
'''
@api_view(['PATCH'])
def update_progress(request):
    print('Y')
    data = request.data['id'] # С фронта {'id':[list]}
    word_ids = [word_id for word_id in data]
    progress = Progress.objects.filter(user_id=request.user.id).filter(translate_id__in=word_ids).order_by('round')
    print(1)
    user_progress = progress.filter(round=progress[0].round).update(round=F('round') + 1)
    print('Y2')
    print('user_progress', user_progress)
    return Response() '''


'''
#class QueryList(ListAPIView):
class QueryList(RetrieveAPIView):
    queryset = Word.objects.all()
    serializer = QuerySerializer

    def retrieve(self, request, pk=None, *args):
        user_id = self.request.user.id
        level = self.kwargs['pk'] # Задаём level
        category = self.queryset.filter(level=level, 
                    word_id__isnull=True).values_list('id', flat=True) #список Категорий
        category = category.order_by('?')[0] #Случайная Категория
        #print(category)
        query = self.queryset.filter(id__in=word_ids(self, category),
                                     active=True).exclude(user_id=user_id)
        #n = (4 - int(level)) * 10 + 20 #кол-во Слов в зависимости от Уровня
        n=2 # для тестирования
        query = query.order_by('?')[:n] # N слов случайной Категории заданного Уровня
        serializer = self.serializer(query, context={'request': request}, many=True)
        return Response(serializer.data) '''


'''
class QueryDetailView(RetrieveAPIView):
    serializer_class = QueryDetailSerializer
    queryset = Query.objects.all()


class WordListView(ListAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.filter(query_id=self.kwargs.get('pk')).order_by('progress__level')[:4]


class ProgressUpdateView(APIView):
    serializer_class = ProgressSerializer

    def get_queryset(self):
        return Word.objects.filter(query_id=self.kwargs.get('pk')).order_by('progress__level')[:4]'''