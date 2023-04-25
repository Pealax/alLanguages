from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.generics import (ListAPIView, ListCreateAPIView)
from .models import *
from .serializers import *

class RulesStudyList(ListAPIView):
    serializer_class = RulesSerializer

    def get_queryset(self):
        user = self.request.user
        ruleslist = Rule.objects.filter(status=1,
            nativ_id=user.native_id,
            learn_id=user.learn_id
        ).exclude(user_id=user.id)
        return ruleslist.order_by('?')[:10]

class UserRulesSet(viewsets.ModelViewSet):
    serializer_class = RulesAnswerSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        if self.action == 'update':
            return Rule.objects.filter(user_id=user_id, status=2)
        else:
            return Rule.objects.filter(user_id=user_id).exclude(status=1)

    def perform_create(self, serializer):
        serializer.save()
        user = self.request.user
        rule = Rule.objects.get(id = serializer.data.get('id'))
        rule.user_id = user.id
        rule.nativ_id = user.native_id
        rule.learn_id = user.learn_id
        rule.save()

class UserRulesCheck(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RulesVerifySerializer
        else:
            return VerifSerializer

    def get_queryset(self):
        user = self.request.user
        ruleslist = Rule.objects.filter(status=0,
            nativ_id=user.native_id,
            learn_id=user.learn_id
        ).exclude(user=user).exclude(verif__user=user)
        return ruleslist.order_by('?')[:1]

    def perform_create(self, serializer):
        serializer.save()
        verifnow = Verif.objects.get(id=serializer.data.get('id'))
        verifnow.user_id = self.request.user.id
        verifnow.save()
        rule_id = serializer.data.get('rule')
        rs = Rule.objects.get(id=rule_id)
        vr = Verif.objects.filter(rule_id=rule_id)
        sum = vr.aggregate(Sum('flag'))['flag__sum']
        count = len(vr)
        if count - sum >= 3:
            rs.status = 2
            rs.save()
        elif 2*sum - count >= 3:
            rs.status = 1
            rs.save()