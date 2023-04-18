from random import choice
from django.db.models import Avg, Min, Max, Sum
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from my_user.models import User #
from .models import *
from .serializers import *

class RulesListView(ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
#+
class UserRulesListView(ListCreateAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        return Rules.objects.filter(userr_id = userid)
    def perform_create(self, serializer):
        serializer.save()
        userid = self.kwargs.get('user_id')
        rules = Rules.objects.get(rules = serializer.data.get('rules')) 
        rules.userr_id = userid
        rules.langnativ_id = User.objects.get(id = userid).native_id
        rules.langlearn_id = User.objects.get(id = userid).learn_id
        rules.save()
#+
class UserRulesCorrectListView(ListAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        ruleslist = Rules.objects.filter(status=2, userr_id = userid)
        return ruleslist
#+
class UserRulesCorrect(RetrieveUpdateAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        rulid = self.kwargs.get('pk')
        ruleslist = Rules.objects.filter(status=2, userr_id = userid)
        spis = ruleslist.values_list("id", flat=True)
        if rulid in spis:
            return Rules.objects.filter(id = rulid)
#+
class UserRulesDeleteListView(ListAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        ruleslist = Rules.objects.filter(userr_id = userid).exclude(status=1)
        return ruleslist
#+
class UserRulesDelete(RetrieveDestroyAPIView):
    serializer_class = RulesAnswerSerializer
    def get_queryset(self):
        userid = self.kwargs.get('user_id')
        rulid = self.kwargs.get('pk')
        ruleslist = Rules.objects.filter(userr_id = userid).exclude(status=1)
        spis = ruleslist.values_list("id", flat=True)
        if rulid in spis:
            return Rules.objects.filter(id = rulid)
#+
class UserRulesVerifiesList(ListAPIView):
    serializer_class = RulesVerifySerializer
    def spis(self):
        userid = self.kwargs.get('user_id')
        ruleslist = Rules.objects.filter(status=0).exclude(userr_id = userid)
        native = User.objects.get(id = userid).native_id
        learn = User.objects.get(id = userid).learn_id
        ruleslist =ruleslist.filter(langnativ_id = native, langlearn_id = learn)
        rspis = ruleslist.values_list("id", flat=True)
        vspis = Verif.objects.filter(userv_id = userid).values_list("rules_id", flat=True)
        spis = rspis.difference(vspis)
        return spis
    def get_queryset(self):
        sp = self.spis()
        ruleslist = Rules.objects.filter(id__in = sp)
        return ruleslist
    
class UserRulesCheck(ListCreateAPIView):
    serializer_class = VerifSerializer
    def rulsel(self):
        userid = self.kwargs.get('user_id')
        ruleslist = Rules.objects.filter(status=0).exclude(userr_id = userid)
        native = User.objects.get(id = userid).native_id
        learn = User.objects.get(id = userid).learn_id
        ruleslist = ruleslist.filter(langnativ_id = native, langlearn_id = learn)
        rspis = ruleslist.values_list("id", flat=True)
        vspis = Verif.objects.filter(userv_id = userid).values_list("rules_id", flat=True)
        spis = rspis.difference(vspis)
        rulsel = choice(spis)
        return rulsel
    def get_queryset(self):
        rs = self.rulsel()
        return Verif.objects.filter(rules_id = rs)
    def perform_create(self, serializer):
        serializer.save()
        rid = serializer.data.get('rules')
        userid = self.kwargs.get('user_id')
        verifnow = Verif.objects.get(date = serializer.data.get('date'))
        verifnow.userv_id = userid
        verifnow.save()
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
