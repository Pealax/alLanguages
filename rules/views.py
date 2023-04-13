from random import choice
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg, Min, Max, Sum
from rest_framework.generics import ListAPIView
from .models import Rules, Answer, Verif
from .serializers import RulesSerializer

class RulesListView(ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

def index(request):
    user = request.user
    ruleslist = Rules.objects.filter(
        langnativ_id = user.native_id,
        langlearn_id = user.learn_id)
    return render(request, 'index.html', {"rlist":ruleslist })

def check(request):
    user = request.user
    ruleslist = Rules.objects.filter(
        langnativ_id = user.native_id,
        langlearn_id = user.learn_id)
    ruleslist = ruleslist.filter(status=0).exclude(userr = user)
    rlist = ruleslist.values_list("id", flat=True)
    rvlist = Verif.objects.filter(userv = user).values_list("rules_id", flat=True)
    list = rlist.difference(rvlist)
    if len(list) == 0:
        return HttpResponse("Нет правил для проверки")
    if request.method == "GET":
        rulsel = ruleslist.get(id=choice(list))
        return render(request, 'check.html', {"rsel":rulsel })
    if request.method == "POST":
        rulsel = ruleslist.get(id=request.POST.get("rsid"))
        verify = Verif()
        verify.flag = request.POST.get("flag")
        verify.comment = request.POST.get("comment")
        verify.rules = rulsel
        verify.userv = user
        verify.save()
        vr = rulsel.verif_set.all()
        sum = vr.aggregate(Sum("flag"))['flag__sum']
        count = len(vr)
        if 2*sum - count >=3 :
            rulsel.status = 1
            rulsel.save()
        if count - sum >=3 :
            rulsel.status = 2
            rulsel.save()
        return HttpResponseRedirect("/api/rules/index")

def create(request):
    user = request.user
    if request.method == "GET":
        return render(request, 'create.html')
    if request.method == "POST":
        rules = Rules()
        rules.rules = request.POST.get("newrule")
        rules.userr_id = user.id
        rules.langnativ_id = user.native_id
        rules.langlearn_id = user.learn_id
        rules.save()
        ans=request.POST.get("ans")
        answnew = ans.split(";")
        for i in range(0,len(answnew)) :
            answer = Answer()
            answer.ans = answnew[i]
            answer.nr_id = rules.id
            answer.save()
        return HttpResponseRedirect("/api/rules/index")

def correct(request):
    ruluser = request.user
    ruleslist = Rules.objects.filter(status=2, userr=ruluser)
    if len(ruleslist) == 0:
        return HttpResponse("Нет правил для коррекции")
    rulsel = choice(ruleslist)
    answ = rulsel.answer_set.all()
    if request.method == "GET":
        return render(request, 'correct.html', {"rlist":ruleslist, "rsel":rulsel })
    if request.method == "POST":
        rulsel.rules = request.POST.get("rule")
        rulsel.status = 0
        rulsel.save()
        rulsel.verif_set.all().delete()
        ans=request.POST.get("ans")
        answupd = ans.split(";")
        k=0
        for a in answ:
            a.ans = answupd[k]
            k+=1
            answ.bulk_update(answ, ['ans'])
        return HttpResponseRedirect("/api/rules/index")

def delete(request):
    ruluser = request.user
    ruleslist = Rules.objects.exclude(status=1).filter(userr=ruluser)
    if request.method == "GET":
        return render(request, 'delete.html', {"rlist":ruleslist })
    if request.method == "POST":
        sel = request.POST.get("rulesselect")
        rul = Rules.objects.get(rules=sel)
        rul.delete()
        return HttpResponseRedirect("/api/rules/index")