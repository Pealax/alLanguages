from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.utils.json import loads, dumps
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

    #def get_queryset

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        serializer = self.serializer(self.queryset.filter(language_id=pk), many=True)
        return Response(serializer.data)


class QueryList(ListAPIView):
    queryset = Word.objects.all()
    serializer_class = QuerySerializer

    '''def get_queryset(self):
        queryset = self.queryset
        queryset['translates'] ='''


class WordViewSet(ModelViewSet):
    queryset = Word.objects.all()
    serializer = WordSerializer

    def list(self, request, *args):
        queries = self.word_ids(None)
        serializer = self.serializer(queries, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args):
        query = self.queryset.get(pk=pk)
        query.words = self.word_ids(query)
        serializer = self.serializer(query, context={'request': request})
        return Response(serializer.data)

    def word_ids(self, query):
        language_ids = [self.request.user.learn_id, self.request.user.native_id]
        word_ids = WordTranslate.objects.filter(language_id__in=language_ids, word__word=query)\
            .values_list('word_id', flat=True)
        ids = [id_ for id_ in word_ids if list(word_ids).count(id_) > 1]

        return self.queryset.filter(id__in=list(set(ids)), active=True)

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




'''def update(self, request, pk=None):
    words = Progress.objects.filter(user_id=request.user.id, word__word_id=pk)

    word_ids = [word_id for word_id in request.data]
    current = words.filter(word_id__in=word_ids, language_id=request.user.learn_id)

    if len(current):
        query_progress = Progress.objects.get(word_id = pk, language_id=request.user.native_id)
        updated_progress = current.filter(round=query_progress.round).update(round=F('round') + 1)
        low_progress = words.exists(round=query_progress.round + 1)
        if low_progress - updated_progress == 0:
            query_progress.round += 1
            query_progress.save()

    return Response()'''


'''class QueryCreateView(CreateAPIView):
    serializer_class = QueryCreateSerializer
    queryset = Query.objects.all()'''


'''class QueryListView(ListAPIView):
    serializer_class = QuerySerializer

    def get_queryset(self):
        language_ids = [self.request.user.learn_id, self.request.user.native_id]
        query_ids = QueryTranslate.objects.filter(language_id__in=language_ids).values_list('query_id', flat=True)
        ids = [id_ for id_ in query_ids if list(query_ids).count(id_) > 1]

        return Query.objects.filter(Q(id__in=list(set(ids))) & Q(active=True))'''

'''
class QueryDetailView(RetrieveAPIView):
    serializer_class = QueryDetailSerializer
    queryset = Query.objects.all()'''

'''
class WordListView(ListAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Word.objects.filter(query_id=self.kwargs.get('pk')).order_by('progress__level')[:4]


class ProgressUpdateView(APIView):
    serializer_class = ProgressSerializer

    def get_queryset(self):
        return Word.objects.filter(query_id=self.kwargs.get('pk')).order_by('progress__level')[:4]'''


@api_view(['PATCH'])
def update_progress(request):
    print('Y')
    data = request.data
    word_ids = [word_id for word_id in data]
    progress = Progress.objects.filter(user_id=request.user.id).filter(translate_id__in=word_ids).order_by('round')
    print(1)
    user_progress = progress.filter(round=progress[0].round).update(round=F('round') + 1)
    print('Y2')
    print('user_progress', user_progress)
    return Response()
