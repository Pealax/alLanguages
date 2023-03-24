from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from language.models import Language, Rules

from language.serializers import LanguageSerializer


class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

def index(request):
    ruleslist = Rules.objects.all()
    return render(request, 'index.html', {"rules":ruleslist})

def create(request):
    if request.method == "GET":
        return render(request, 'create.html')
    if request.method == "POST":
        rules = Rules()
        rules.rules = request.POST.get("newrule")
        rules.save()
        return HttpResponseRedirect("/api/language/index")