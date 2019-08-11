from django.shortcuts import render
from django.http import HttpResponse
from . import models
import json
# Create your views here.
def add_note(request):
    if request.method == "GET":
        return render(request,'add_note.html')
    elif request.method == "POST":
        title = request.POST.get("title","")
        content = request.POST.get("content","")
        author =  request.session['userinfo']['id']
        note = models.Note()
        note.title = title
        note.content = content
        note.author = models.User.objects.get(id = author)
        note.save()
        return HttpResponse("提交成功")

def home(request):
    return render(request,'home.html')

def show(request):
    get_author = request.session['userinfo']['id']
    author = models.User.objects.get(id = get_author)
    notes = author.note_set.all()
    arr = []
    for note in notes:
        dic = {
            'title':note.title,
            'content':note.content
        }
        arr.append(dic)
    res = json.dumps(arr)
    return HttpResponse(res)