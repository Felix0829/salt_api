# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render,HttpResponse,render_to_response
import salt_api as api
# Create your views here.

def saltstack(request):
    type = str(request.POST.get("type")).strip()
    host_key = str(request.POST.get("host_key")).strip()
    commd = str(request.POST.get("commd")).strip()
    alert = """alert("系统不识别该您输入的信息，请检查。");"""
    from_list = {
        "type": type,
        "host_key": host_key,
        "commd": commd,
    }
    sapi = api.SaltAPI(url='https://192.168.10.69:8000', username='jianfei', password='jianfei')
    if request.method == "POST":
        if type == "cmd.run":
            commd_log = sapi.cmd_run(tgt=host_key,fun="cmd.run",arg=commd)
            false_keys = false(list(commd_log["return"][0].keys()))
            return render_to_response('salt_index.html', {'commd_log': commd_log["return"][0], 'from_list': from_list,'false_keys':false_keys,})
        elif type == "cmd.script" and type != "test.ping":
            commd_log = sapi.test_ping(tgt=host_key,fun=type)
            false_keys = false(list(commd_log["return"][0].keys()))
            # commd_log = api.Salt().cmd_run(host_key="*", type="cmd.script", commd="salt://test.sh")
            return render_to_response('salt_index.html', {'commd_log': commd_log, 'from_list': from_list,'false_keys':false_keys,})
        elif type == "test.ping":
            commd_log = sapi.test_ping(tgt=host_key,fun=type)
            false_keys = false(list(commd_log["return"][0].keys()))
            # print commd_log["return"][0]
            return render_to_response('salt_index.html', {'commd_log': commd_log["return"][0], 'from_list': from_list,'false_keys':false_keys,})
        else:
            from_list["alert"] = alert
            return render_to_response('salt_index.html', {'from_list': from_list,})
    elif request.method == "GET":
        commd_log = sapi.test_ping(tgt="*", fun="test.ping")
        false_keys = false(list(commd_log["return"][0].keys()))
        return render_to_response('salt_index.html', {'from_list':{'type':'test.ping','*':"test.ping","commd":"none"},'false_keys':false_keys,})

def false(key):
    sapi = api.SaltAPI(url='https://192.168.10.69:8000', username='jianfei', password='jianfei')
    all_keys=sapi.list_all_key()[0]
    # commd_log = sapi.test_ping(tgt="*", fun="test.ping")
    # true_keys = list(commd_log["return"][0].keys())
    true_keys = key
    false_keys = list(set(true_keys) ^ set(all_keys))
    # print false_keys
    return false_keys