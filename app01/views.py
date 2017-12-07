from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from app01 import models
from django.contrib import auth
from django.forms import ModelForm
# Create your views here.


def log_in(request):
    if request.method=="GET":
        return render(request,"login.html")

    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=auth.authenticate(username=username,password=password)
        if not user:
            return redirect("/log_in/")
        else:
            auth.login(request,user)
            return redirect("/index/")

def index(request):
    permission=request.user.is_superuser
    if permission:
        questionnaire_list=models.Questionnaire.objects.all()
        return render(request,"index.html",{"questionnaire_list":questionnaire_list})
    else:
        return HttpResponse("没有权限访问")


def add_questionnaire(request):
    if request.method=='GET':
        classes = models.Classes.objects.all()
        admin = models.UserInfo.objects.filter(is_superuser=1).all()
        return render(request, "add_questionnaire.html", {"classes": classes, "admin": admin})
    elif request.method=="POST":
        title=request.POST.get("title")
        class1=request.POST.get("class1")
        creator=request.POST.get("creator")
        models.Questionnaire.objects.create(title=title,class1_id=class1,creator_id=creator)
        return redirect("/index/")


def del_questionnaire(request):
    del_response={"status":None}
    qnr_id=request.POST.get("qnr_id")
    if qnr_id:
        models.Questionnaire.objects.filter(id=qnr_id).delete()
        del_response["status"]=True
    else:
        del_response["error_message"]="滚蛋"
    return JsonResponse(del_response,safe=True)


class Question(object):
    def __init__(self,data):
        self.data=data

    def __iter__(self):
        for question in self.data:
            yield question

class QuestionModelForm(ModelForm):
    class Meta:
        model=models.Question
        fields=["caption","tp"]


class OptionModelForm(ModelForm):
    class Meta:
        model=models.Option
        fields=["name","value"]


def edit_qnr(request,qnr_id):

    def inner():
        questions=models.Questionnaire.objects.filter(id=qnr_id).first().question_set.all()
        if not questions:
            form=QuestionModelForm()
            yield {"form":form,"obj":None,"option_class":"hide","options":None}
        else:
            for question in questions:
                form=QuestionModelForm(instance=question)
                tmp= {"form":form,"obj":question,"option_class":"hide","options":None}
                if question.tp==2:
                    tmp["option_class"]=""
                    def inner_loop(que):
                        option_list= models.Option.objects.filter(question=que)
                        for option in option_list:
                            yield {"form":OptionModelForm(instance=option),"obj":option}
                    tmp["options"]=inner_loop(question)
                yield tmp
    return render(request,"edit_qnr.html",{"forms":inner()})