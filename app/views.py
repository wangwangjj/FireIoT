from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from .models import Data,Data1
from datetime import datetime
import MySQLdb

# Create your views here.

def homepage(request):
    template = get_template('index.html')
    now = datetime.now()
    html = template.render(locals())
    
    return HttpResponse(html)

def test(request):
    json_list = [];
    goods = Data.objects.order_by('-id')
    for good in goods:
        json_dict={}
        json_dict["id"] = good.id
        json_dict["device"] = good.device
        json_dict["jihao"] = good.jihao
        json_dict["huilu"] = good.huilu
        json_dict["addr"] = good.addr
        json_dict["item"] = good.item
        json_dict["state"] = good.state
        json_dict["pub_date"] = good.pub_date
        json_list.append(json_dict)
    import json
    return HttpResponse(json.dumps(json_list),content_type="application/json")

def check(request):
    db = MySQLdb.connect("localhost","root","962424lgj","CHECK",charset='utf8')
    cursor = db.cursor()
    sql="update CheckOnline set STATUS=\"1\";"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    return HttpResponse("ok")

def xunjian(request):
    db = MySQLdb.connect("localhost","root","962424lgj","CHECK",charset='utf8')
    cursor = db.cursor()
    sql="update CheckOnline set STATUS=\"2\";"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    return HttpResponse("ok")

def test1(request):
    json_list = [];
    goods = Data1.objects.order_by('-id')
    for good in goods:
        json_dict={}
        json_dict['state'] = good.state
        json_dict['pub_date'] = good.pub_date
        json_list.append(json_dict)
    import json
    return HttpResponse(json.dumps(json_list),content_type="application/json")
