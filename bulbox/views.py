import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from bulbox.models import question
from bulbox.models import IWanna
from bulbox.models import Comments
from django.utils import timezone
from django.core import mail
from datetime import datetime, timedelta

def format_datetime(dt):
    cutoff_date = datetime(2023, 10, 20)

    if dt < cutoff_date:
        return dt.strftime("%Y-%m-%d")
    else:
        return dt.strftime("%Y/%m/%d %H:%M")
    

def postYouAskMe(request):
    if(request.method == 'POST'):
        json_param = json.loads(request.body.decode())
        if json_param:
            _ques = json_param.get('ques', 0)
            _now = timezone.now()
            q = question(ques=_ques, quesTime=_now)
            q.save()

            subject = "Bulbox - 新的提问"
            message = "收到一条新提问：\n" + _ques + "\n\n提问时间：\n" + \
                _now.strftime("%Y-%m-%d %H:%M:%S")
            sendMess(subject, message)

        else:
            return HttpResponse('no params')
        return HttpResponse('Successfully Submit')
    else:
        return HttpResponse("NOT POST METHOD")


def getToken(request):
    token = get_token(request)
    return HttpResponse(json.dumps({'token': token}))


def getYouAskMe(request):
    res = question.objects.order_by("-id").all()
    responseData = []
    print(format_datetime(res[1].quesTime))
    for i in res:
        print(format_datetime(i.quesTime))
        ansTime = ""
        if i.ansTime is not None: 
            ansTime = format_datetime(i.ansTime)
        temp = {
            'id': i.id,
            'ques': i.ques,
            'ans': i.ans,
            'display': i.display,
            'quesTime': format_datetime(i.quesTime),
            'ansTime': ansTime
        }
        responseData.append(temp)

    return HttpResponse(json.dumps(responseData))


def ansYouAskMe(request):
    if(request.method == 'POST'):
        json_param = json.loads(request.body.decode())
        for i in json_param:
            print(i)

    else:
        return HttpResponse("NOT POST METHOD")


def getIAskYouQues(request):
    # Get all question in the IAskYou

    res = IWanna.objects.order_by('-id').all()
    responseData = []
    for i in res:
        comments = Comments.objects.filter(quesId=i.id).count()
        temp = {
            'id': i.id,
            'ques': i.ques,
            'commentsNum': comments
        }
        responseData.append(temp)

    return HttpResponse(json.dumps(responseData))


def getIAskYouDetails(request):
    # Get the details of one question
    if(request.method == 'POST'):

        json_param = json.loads(request.body.decode())
        if json_param:

            res = Comments.objects.filter(quesId=json_param.get('quesId', 0))
            ques = IWanna.objects.get(id=json_param.get('quesId', 0))

            responseData = {'ques': '', 'comments': []}

            responseData['ques'] = ques.ques

            tempList = []
            for i in res:
                temp = {
                    'id': i.id,
                    'quesId': i.quesId,
                    'content': i.content,
                    'display': i.display,
                    'ansTime':  format_datetime(i.subTime),
                }
                tempList.append(temp)

            responseData['comments'] = tempList

            return HttpResponse(json.dumps(responseData))
        else:
            return HttpResponse('no params')
    else:
        return HttpResponse("NOT POST METHOD")


def postIAskYou(request):
    # other one submit the ans to database
    if(request.method == 'POST'):
        json_param = json.loads(request.body.decode())
        if json_param:
            _quesId = json_param.get('quesId', 0)
            _content = json_param.get('content', 0)
            _now = timezone.now()
            entry = Comments(quesId=_quesId, content=_content,
                             subTime=_now)
            entry.save()
            
            subject = "Bulbox - 新的回答"
            _quesContent = IWanna.objects.get(
                id=json_param.get('quesId', 0)).ques

            message = "收到一条新回答，关于问题：\n"+_quesContent
            message += "\n\n回答内容为：\n" + _content + "\n\n回答时间：\n" + \
                _now.strftime("%Y-%m-%d %H:%M:%S")
            sendMess(subject, message)

        else:
            return HttpResponse('no params')
        return HttpResponse('Successfully Submit')
    else:
        return HttpResponse("NOT POST METHOD")


def subIAskYou(request):
    # I submit a question to the database

    return


def sendMess(subject, message):
    mail.send_mail(
        subject=subject,
        message=message,
        from_email="3134712772@qq.com",
        recipient_list=["1079729701@qq.com"],
        fail_silently=False,
    )
    return
