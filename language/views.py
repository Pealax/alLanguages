from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from language.models import Language, Rules, Answer
from language.serializers import LanguageSerializer


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

def index(request):
    ruleslist = Rules.objects.all()
    answers = Answer.objects.all()
    return render(request, 'index.html', {"rlist":ruleslist, "answ":answers })

def create(request):
    if request.method == "GET":
        return render(request, 'create.html')
    if request.method == "POST":
        rules = Rules()
        rules.rules = request.POST.get("newrule")
        rules.save()
        Answer.objects.bulk_create([
            Answer(ans=request.POST.get("ans1"), nr_id=rules.id),
            Answer(ans=request.POST.get("ans2"), nr_id=rules.id),
            Answer(ans=request.POST.get("ans3"), nr_id=rules.id),
            ])
        return HttpResponseRedirect("/api/language/index")