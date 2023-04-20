from random import choice
from django.db.models import Avg, Min, Max, Sum
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from .models import *
from .serializers import *

class RulesListView(ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

class UserRulesListView(ListCreateAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.request.user.id
        return Rules.objects.filter(userr = userid)
    def perform_create(self, serializer):
        serializer.save()
        user = self.request.user
        rules = Rules.objects.get(id = serializer.data.get('id'))
        rules.userr_id = user.id
        rules.langnativ_id = user.native_id
        rules.langlearn_id = user.learn_id
        rules.save()

class UserRulesCorrectListView(ListAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.request.user.id
        ruleslist = Rules.objects.filter(status=2, userr_id = userid)
        return ruleslist

class UserRulesCorrect(RetrieveUpdateAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.request.user.id
        rulid = self.kwargs.get('pk')
        ruleslist = Rules.objects.filter(status=2, userr_id = userid)
        spis = ruleslist.values_list("id", flat=True)
        if rulid in spis:
            return Rules.objects.filter(id = rulid)

class UserRulesDeleteListView(ListAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.request.user.id
        ruleslist = Rules.objects.filter(userr_id = userid).exclude(status=1)
        return ruleslist

class UserRulesDelete(RetrieveDestroyAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.request.user.id
        rulid = self.kwargs.get('pk')
        ruleslist = Rules.objects.filter(userr_id = userid).exclude(status=1)
        spis = ruleslist.values_list("id", flat=True)
        if rulid in spis:
            return Rules.objects.filter(id = rulid)

class UserRulesVerifiesList(ListAPIView):
    serializer_class = RulesVerifySerializer
    def spis(self):
        user = self.request.user
        ruleslist = Rules.objects.filter(status=0).exclude(userr_id = user.id)
        native = user.native_id
        learn = user.learn_id
        ruleslist =ruleslist.filter(langnativ_id = native, langlearn_id = learn)
        rspis = ruleslist.values_list("id", flat=True)
        vspis = Verif.objects.filter(userv_id = user.id).values_list("rules_id", flat=True)
        spis = rspis.difference(vspis)
        return spis
    def get_queryset(self):
        sp = self.spis()
        ruleslist = Rules.objects.filter(id__in = sp)
        return ruleslist
    
class UserRulesCheck(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RulesVerifySerializer
        return VerifSerializer
    def rulsel(self):
        user = self.request.user
        ruleslist = Rules.objects.filter(status=0).exclude(userr_id = user.id)
        native = user.native_id
        learn = user.learn_id
        ruleslist = ruleslist.filter(langnativ_id = native, langlearn_id = learn)
        rspis = ruleslist.values_list("id", flat=True)
        vspis = Verif.objects.filter(userv_id = user.id).values_list("rules_id", flat=True)
        spis = rspis.difference(vspis)
        rulsel = choice(spis)
        return rulsel
    def get_queryset(self):
        rs = self.rulsel()
        querry = Rules.objects.filter(id = rs)
        return querry
    def perform_create(self, serializer):
        serializer.save()
        userid = self.request.user.id
        verifnow = Verif.objects.get(id = serializer.data.get('id'))
        verifnow.userv_id = userid
        verifnow.save()
        rid = serializer.data.get('rules')
        rs = Rules.objects.get(id = rid)
        vr = Verif.objects.filter(rules_id=rid)
        sum = vr.aggregate(Sum("flag"))['flag__sum']
        count = len(vr)
        if 2*sum - count >=3 :
            rs.status = 1
            rs.save()
        if count - sum >=3 :
            rs.status = 2
            rs.save()