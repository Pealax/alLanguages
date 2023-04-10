from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django.db.models import Avg, Min, Max, Sum
from .models import Rules, Answer, Verif
from .serializers import RulesSerializer

class RulesListView(ListAPIView):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

def index(request):
    ruleslist = Rules.objects.all()
    return render(request, 'index.html', {"rlist":ruleslist })

def check(request):
    ruluser = request.user
    ruleslist = Rules.objects.exclude(userr=ruluser)
    ruleslist = ruleslist.filter(status=0)
    if request.method == "GET":
        return render(request, 'check.html', {"rlist":ruleslist })
    if request.method == "POST":
        verify = Verif()
        verify.flag = request.POST.get("flag")
        verify.comment = request.POST.get("comment")
        sel = request.POST.get("rulesselect")
        rulsel = Rules.objects.get(rules=sel)
        verify.rules = rulsel
        verify.userv = ruluser
        verify.save()
        vr = rulsel.verif_set.all()
        sum = vr.aggregate(Sum("flag"))['flag__sum']
        count = vr.count()
        if sum >=3 :
            rulsel.status = 1
            rulsel.save()
        if count - sum >=3 :
            rulsel.status = 2
            rulsel.save()
    return HttpResponseRedirect("/api/rules/index")

def create(request):
    if request.method == "GET":
        return render(request, 'create.html')
    if request.method == "POST":
        rules = Rules()
        rules.rules = request.POST.get("newrule")
        rules.userr = request.user
        rules.save()
        Answer.objects.bulk_create([
            Answer(ans=request.POST.get("ans1"), nr_id=rules.id),
            Answer(ans=request.POST.get("ans2"), nr_id=rules.id),
            Answer(ans=request.POST.get("ans3"), nr_id=rules.id),
            ])
    return HttpResponseRedirect("/api/rules/index")

def correct(request):
    ruluser = request.user
    ruleslist = Rules.objects.filter(userr=ruluser)
    ruleslist = ruleslist.filter(status=2)
    if request.method == "GET":
        return render(request, 'correct.html', {"rlist":ruleslist })
    if request.method == "POST":
        sel = request.POST.get("rulesselect")
        upd = request.POST.get("rule")
        answupd =[request.POST.get("ans1"),
            request.POST.get("ans2"),
            request.POST.get("ans3")]
        rul = Rules.objects.get(rules=sel)
        answ = rul.answer_set.all()
        rul.rules = upd
        rul.status = 0
        rul.save()
        k=0
        for a in answ:
            a.ans = answupd[k]
            k+=1
        answ.bulk_update(answ, ['ans'])
    return HttpResponseRedirect("/api/rules/index")

def delete(request):
    ruluser = request.user
    ruleslist = Rules.objects.filter(userr=ruluser)
    ruleslist = ruleslist.exclude(status=1)
    if request.method == "GET":
        return render(request, 'delete.html', {"rlist":ruleslist })
    if request.method == "POST":
        sel = request.POST.get("rulesselect")
        rul = Rules.objects.get(rules=sel)
        rul.delete()
    return HttpResponseRedirect("/api/rules/index")