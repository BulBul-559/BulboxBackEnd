from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.


class question(models.Model):
    ques = models.CharField(max_length=300)
    quesTime = models.DateTimeField(null=True)
    ans = models.CharField(max_length=2000, null=True)
    ansTime = models.DateTimeField(null=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        question_text = """
        ques: %s,
        quesTime: %s,
        ans: %s,
        ansTime: %s,
        display: %s
        """ % (self.ques, self.quesTime, self.ans, self.ansTime, self.display)

        return question_text


class IWanna(models.Model):
    ques = models.CharField(max_length=300)
    quesTime = models.DateTimeField(null=True)

    def __str__(self):
        IWanna_text = """
        ques: %s,
        quesTime: %s,
        """ % (self.ques, self.quesTime)
        return IWanna_text


class Comments(models.Model):
    quesId = models.IntegerField(null=False)
    content = models.CharField(max_length=2000)
    subTime = models.DateTimeField(null=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        Comments_text = """
        quesId: %s,
        content: %s,
        subTime: %s,
        display: %s
        """ % (self.quesId, self.content, self.subTime, self.display)

        return Comments_text
