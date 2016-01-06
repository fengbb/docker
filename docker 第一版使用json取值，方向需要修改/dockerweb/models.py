from django.db import models
import json

# Create your models here.
class User(models.Model):
    username = models.CharField(u'用户名',max_length=30)
    password = models.CharField(u'用户密码',max_length=100)
    email = models.EmailField(u'电子邮箱')
    #docker_machine = models.ForeignKey(Docker)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
class Docker(models.Model):
    name = models.CharField(u'主机名',max_length=30)
    user = models.ForeignKey(User)
    describe = models.CharField(u'主机描述',max_length=50)
    def __str__(self):
        return self.name,self.user
    class Meta:
        verbose_name = '主机'
        verbose_name_plural = '主机管理'
'''
class pods(models.Model):
    name = models.CharField(max_length=30)
    generateName = models.CharField(max_length=30)
    namespace = models.CharField(max_length=30)
    selfLink  = models.CharField(max_length=30)
    uid = models.CharField(max_length=30)
    resourceVersion = models.CharField(max_length=30)
    creationTimestamp = models.CharField(max_length=30)
    run = models.CharField(max_length=30)
    containers_name = models.CharField(max_length=30)
    containers_image = models.CharField(max_length=30)
    containers_ports_containerPort = models.CharField(max_length=30)
    containers_ports_protocol = models.CharField(max_length=30)
    nodename = models.IPAddressField()
    phase = models.CharField(max_length=30)
    hostip = models.CharField(max_length=30)
    podip = models.CharField(max_length=30)
    starttime = models.CharField(max_length=30)
    image = models.CharField(max_length=30)
    imageID = models.CharField(max_length=100)
    containerID = models.CharField(max_length=100)
    def save_json(json_str):
        obj = json.loads(json_str)
        sql = 'insert into pods values (%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s)' % (obj['name']obj['generateName']obj['namespace']obj['selfLink']obj['uid']obj[' resourceVersion']obj['creationTimestamp']obj['run']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj[''])

'''