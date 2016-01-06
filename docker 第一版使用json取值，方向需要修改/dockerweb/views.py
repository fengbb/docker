#-*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
#from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.contrib import auth
from dockerweb.forms import UserForm,UserRegistForm
from dockerweb.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
#from gevent import monkey
#monkey.patch_all()
from django import *
#from werkzeug.exceptions import BadRequest,Unauthorized
#import wssh
#from wssh.server import WSSHBridge
import json
import ast
import simplejson
import os
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
# Create your views here.
@login_required
def index(request):
    username = request.session.get('username','anybody')
#    print (username)
    return render_to_response('index.html',{'username': username})
def base(request):
    return render_to_response('base.html')
def regist(request):
    if request.method == 'POST':
        urf = UserRegistForm(request.POST)
        #urf = UserRegistForm(request.POST)
        if urf.is_valid():
            user = urf.cleaned_data['username']
            passwd = urf.cleaned_data['password']
            emailaddress = urf.cleaned_data['email']
            print (urf.cleaned_data['username'])
            print (urf.cleaned_data['password'])
            print (urf.cleaned_data['email'])
            User.objects.create(username=user, password=passwd, email=emailaddress)
            return render_to_response('register_success.html')
    else:
        urf = UserRegistForm()
    return render_to_response('regist.html', {'urf': urf})
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print (username)
        #print (password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                auth.login(request,user)
                request.session.set_expiry(60*30)
                request.session['username'] = username
                #print 'session expires at :',request.session.get_expiry_date()
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})
        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
def shellinabox(request):
    ipaddr = "192.168.40.203"
    shellinabox_port = int(8800)
    #url = 'http://%s:%s' % (ipaddr,shellinabox_port)
    url = 'https://%s:%s' % (ipaddr,shellinabox_port)
   # return HttpResponseRedirect(url)
   # username = 'root'
    #password = 'Abcd1234'
    #boxInfo = {'url':url, 'username':username, 'password':password}
    return HttpResponseRedirect(url)

def getImagesJson(request):
    #json_images_data = utils.get_image_json()
    url = "http://192.168.153.86:4243/images/json" #定义url地址
    data = urllib.request.urlopen(url).read().decode() #取得接口json数据
    return HttpResponse(data,content_type='application/json')
def getContainersJson(request):
    #json_container_data = utils.get_container_json()
    url = "http://192.168.153.86:4243/containers/json?all=1"
    data = urllib.request.urlopen(url).read().decode()
    return HttpResponse(data,content_type='application/json')
def getImageDetaileJson(request):
    imageid = request.get_full_path().split('/')[2]
    url = "http://192.168.153.86:4243/images/%s/json" %(imageid)
    data = urllib.request.urlopen(url).read().decode()
    return HttpResponse(data,content_type='application/json')
@login_required
def images(request):
    #print (request.get_full_path())
    username = request.session.get('username','anybody')
    #print (username)
    return render_to_response('images.html')
@login_required
def imagedetaile(request):
    #print (request.get_full_path())
    imageid = request.get_full_path().split('/')[2]
    return render_to_response('imagedetaile.html',{'imageid': imageid})
@login_required
def containers(request):
    return render_to_response('containers.html')

def test(request):
    #json_images_data = utils.get_image_json()
    #dd = utils.test()
    #dd = {'b':789,'c':456,'a':123,'d':'1234'}
    test_json_data = [
    {
        "Id": "e9ff33e7e5b9a683ab735bbe99450c50bd0b64c4e414d12c94ff93b345d3bb18",
        "ParentId": "22218d75fdd7dfba85feb60f8165eecb5ba13b9364b07ec2b8cd76e887bd6d78",
        "RepoTags": [
            "docker.io/swarm:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1449709381,
        "Size": 0,
        "VirtualSize": 17146714,
        "Labels": 'null'
    },
    {
        "Id": "32653661039ddb04d405db13861f63660e4dfa3b332e6226b2a0f1ad0ce71aa3",
        "ParentId": "",
        "RepoTags": [
            "docker.io/alpine:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1449682169,
        "Size": 5248653,
        "VirtualSize": 5248653,
        "Labels": 'null'
    },
    {
        "Id": "d55e68e6cc9c7f78f1c02001e1a5ce76511db044c659e5c0a4275c54473f2869",
        "ParentId": "b207c06aba70227e0a2561bb7df20a5fd1310901da98ecc6f4da7dccdc40d961",
        "RepoTags": [
            "docker.io/ubuntu:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1449599913,
        "Size": 0,
        "VirtualSize": 187894764,
        "Labels": 'null'
    },
    {
        "Id": "6ffc02088cb870652eca9ccd4c4fb582f75b29af2879792ed09bb46fd1c898ef",
        "ParentId": "0d30b5fc3b42ebbeaa8a57708b981ff2a8dc150b24e5a8042fbf40264e9181a7",
        "RepoTags": [
            "docker.io/nginx:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1449598887,
        "Size": 0,
        "VirtualSize": 133816084,
        "Labels": 'null'
    },
    {
        "Id": "b6a2f7546a7f961688c29c05de47ce6c559665e67d8c7fb6b94affaba80c5278",
        "ParentId": "1b4531fc042729dd41507885aa304544763603c7196afee954dd960c2690d5e3",
        "RepoTags": [
            "docker.io/ehazlett/docker-proxy:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1441494155,
        "Size": 0,
        "VirtualSize": 7840701,
        "Labels": 'null'
    },
    {
        "Id": "6c4579af347b649857e915521132f15a06186d73faa62145e3eeeb6be0e97c27",
        "ParentId": "e244e638e26e77a8b08da462b1cb92811ed6d3d2874286368afcef7717ed9475",
        "RepoTags": [
            "gcr.io/google_containers/pause:0.8.0",
            "gcr.io/google_containers/pause:latest",
            "docker.io/kubernetes/pause:latest"
        ],
        "RepoDigests": 'null',
        "Created": 1405753352,
        "Size": 0,
        "VirtualSize": 239840,
        "Labels": 'null'
    }
    ]
    return HttpResponse(json.dumps(test_json_data),content_type='application/json')
    #return render_to_response('test.html')