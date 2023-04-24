import random
from django.db.models import Avg, Min, Max, Sum
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView
)
from .models import *
from .serializers import *

class RulesListView(ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

class MyRulesListView(ListCreateAPIView):
    serializer_class = RulesSerializer
    def get_queryset(self):
        user_id = self.request.user.id
        return Rules.objects.filter(user_id=user_id, status=1)

class UserRulesCurrentList(ListCreateAPIView):
    serializer_class = RulesAnswerSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Rules.objects.filter(user_id=user_id).exclude(status=1)

    def perform_create(self, serializer):
        serializer.save()
        user = self.request.user
        rule = Rules.objects.get(id = serializer.data.get('id'))
        rule.user_id = user.id
        rule.nativ_id = user.native_id
        rule.learn_id = user.learn_id
        rule.save()

class UserRuleCorrect(RetrieveUpdateAPIView):
    serializer_class = RulesAnswerSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        rule_id = self.kwargs.get('pk')
        return Rules.objects.filter(id=rule_id, user_id=user_id, status=2)

class UserRuleDelete(RetrieveDestroyAPIView):
    serializer_class = RulesAnswerSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        rule_id = self.kwargs.get('pk')
        return Rules.objects.filter(id=rule_id, user_id=user_id,).exclude(status=1)

class UserRulesCheck(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RulesVerifySerializer
        else:
            return VerifSerializer

    def spis(self):
        user = self.request.user
        ruleslist = Rules.objects.filter(status=0).exclude(user_id=user.id)
        native = user.native_id
        learn = user.learn_id
        ruleslist =ruleslist.filter(nativ_id=native, learn_id=learn)
        rspis = ruleslist.values_list('id', flat=True)
        vspis = Verif.objects.filter(user_id=user.id).values_list('rule_id', flat=True)
        spis = rspis.difference(vspis)
        return spis

    def get_queryset(self):
        spis = [item for item in self.spis()]
        k = len(spis)
        if k > 5:
            k=5
            spis = random.sample(spis, k=k)
        ruleslist = Rules.objects.filter(id__in=spis)
        return ruleslist

    def perform_create(self, serializer):
        serializer.save()
        user_id = self.request.user.id
        verifnow = Verif.objects.get(id=serializer.data.get('id'))
        verifnow.user_id = user_id
        verifnow.save()
        rule_id = serializer.data.get('rule')
        rs = Rules.objects.get(id=rule_id)
        vr = Verif.objects.filter(rule_id=rule_id)
        sum = vr.aggregate(Sum('flag'))['flag__sum']
        count = len(vr)
        if count - sum >=3:
            rs.status = 2
            rs.save()
        elif 2*sum - count >=3:
            rs.status = 1
            rs.save()