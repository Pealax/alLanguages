from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.utils.json import loads, dumps # вероятно, не нужны
from rest_framework.views import APIView

from word.models import Word, WordTranslate, Progress
from word.serializers import WordSerializer, QuerySerializer, TranslateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class Translates (APIView):
    queryset = WordTranslate.objects.all()
    serializer = TranslateSerializer

    def get(self, request, *args, **kwargs):
        language = self.kwargs['pk']
        serializer = self.serializer(self.queryset.filter(language_id=language), many=True)
        return Response(serializer.data)

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
        return Response(serializer.data)


class WordViewSet(ModelViewSet):
    queryset = Word.objects.all()
    serializer = WordSerializer

    def list(self, request, *args):
        queries = self.queryset.filter(id__in=word_ids(self, None), active=True)
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args):
        query = self.queryset.filter(id__in=word_ids(self, pk), active=True)
        serializer = self.serializer(query, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request, *args):
        data = request.data
        data['user'] = request.user.id
        serializer = self.serializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            print(serializer.error_messages)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
        return Response()

def word_ids(self, category): #Выбор Word у которых есть Translate на обоих языках
    language_ids = [self.request.user.learn_id, self.request.user.native_id]
    ids1 = WordTranslate.objects.filter(language_id=language_ids[0],
                word__word=category).values_list('word_id', flat=True)
    ids2 = WordTranslate.objects.filter(language_id=language_ids[1],
                word__word=category).values_list('word_id', flat=True)
    word_ids = set(ids1)
    word_ids.intersection_update(ids2)
    return list(word_ids)

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
    return Response()

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