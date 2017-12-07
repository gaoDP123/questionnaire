from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Classes(models.Model):
    '''
    班级表
    '''
    name=models.CharField(verbose_name="班级名称",max_length=12)
    population=models.IntegerField(verbose_name="班级人数")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="班级表"

class UserInfo(AbstractUser):
    name=models.CharField(verbose_name="真实姓名",max_length=20)
    class1=models.ForeignKey(verbose_name="所属班级",to="Classes",null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="用户表"

class Questionnaire(models.Model):
    title=models.CharField(verbose_name="问卷标题",max_length=32)
    class1=models.ForeignKey(verbose_name="问卷所属班级",to="Classes")
    creator=models.ForeignKey(verbose_name="创建者",to="UserInfo")
    number_people = models.IntegerField(verbose_name="已参加人数", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="问卷调查表"

class Question(models.Model):
    caption=models.CharField(verbose_name="问题",max_length=255)
    question_type=(
        (1,"分数"),
        (2,"单选"),
        (3,"评论")
    )
    tp=models.IntegerField(choices=question_type,)
    questionnaire=models.ForeignKey(verbose_name="关联问卷",to="Questionnaire")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name_plural="问题表"

class Option(models.Model):
    name=models.CharField(verbose_name="自定义选项",max_length=128)
    value=models.IntegerField(verbose_name="自定义分数")
    question=models.ForeignKey(verbose_name="关联问题",to="Question")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="选项表"

class Result(models.Model):
    content=models.CharField(verbose_name="内容",null=True,blank=True,max_length=255)
    score=models.IntegerField(verbose_name="分数",null=True,blank=True)
    user=models.ForeignKey(verbose_name="被调查人",to="UserInfo")
    question=models.ForeignKey(verbose_name="所属问题",to="Question")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural="结果表"