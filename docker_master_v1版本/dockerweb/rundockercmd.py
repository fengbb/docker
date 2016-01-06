#-*-coding:utf-8-*-
import paramiko
import time
import random
import os
import sys
###################解决django在其他地方使用admin的models和temple##########################
#from django.conf import settings                                                       #
#settings.configure()
#os.environ.setdefault("DJANGO_SETTINGS_MODULE",'docker.settings')
#########################################################################################

###############解决django在其他地方连接mysql，报错###############################
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'docker.settings')             ###
#################################################################################
from dockerweb.models import Container,ContainerIp                                            #
#函数创建一个容器
from django.conf import settings
print(settings.IMAGEDOMAIN)
imagedomain = settings.IMAGEDOMAIN
print(imagedomain)
def sshClient(ip,dockerpwd):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,password=dockerpwd,username="root")
    #print(ssh)
    return ssh

def createContainer(sshobject,dockername,imagename,ip,ip1,ip2,ip3):
    ##启动一台容器的命令
    msg = ''
    #cmd = 'docker run -itd --name %s --net=none hc.docker.io:5000/%s  /bin/bash' % (dockername,imagename)
    cmd = 'docker run -itd --name %s --net=none %s:5000/%s  /bin/bash' % (dockername,imagedomain,imagename)
    print (cmd)
    stdinstart,stdoutstart,stderrstart = sshobject.exec_command(cmd)
    print(dockername,imagedomain,imagename)
    print(stderrstart.read().decode())
    #返回创建docker的id
    containerid = stdoutstart.read().decode()
    time.sleep(10)
    #配置容器ip,随机生成一个没有使用的ip
    #while True:
    #    lastip = random.randint(20,200)
    #    ip = '192.168.153.%s' %(lastip)
    #    if_ip_exist = Container.objects.filter(containerhost=ip)
    #    if if_ip_exist:
    #        lastip = random.randint(20,200)
    #        continue
    #    else:
    #        break
    #print (ip)
    #更改容器ip的命令
    cmdsetip = 'pipework br0 %s %s/24@%s.%s.%s.1' %(dockername,ip,ip1,ip2,ip3)
    stdinnet,stdoutnet,stderrnet = sshobject.exec_command(cmdsetip)
    print(cmdsetip)
    #启动ssh命令
    cmdstartssh = 'docker exec -d %s /root/startssh.sh' %(dockername)
    stdinssh,stdoutssh,stderrssh = sshobject.exec_command(cmdstartssh)
    #更改容器password
    basepassword = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789',8))
    cmdchagepw = 'docker exec -d %s /root/cpasswd.sh %s' %(dockername,basepassword)
    stdincp,stdoutcp,stderrcp = sshobject.exec_command(cmdchagepw)
    #print(basepassword)
    #print (cmdchagepw)
    #print(cmdstartssh)
    return containerid,basepassword
def restartContainer(sshobject,dockerid,containerip,password):
    cmdrestartcontainer = 'docker restart %s' % (dockerid)
    stdinrestart,stdoutrestart,stderrrestart = sshobject.exec_command(cmdrestartcontainer)
    #print(stdoutrestart.read().decode())
    stdoutrestart = stdoutrestart.read().decode()
    ipfirst = containerip.split('.')[:3]
    ip1,ip2,ip3 = (ipfirst)
    cmdsetip = 'pipework br0 %s %s/24@%s.%s.%s.1' %(dockerid,containerip,ip1,ip2,ip3)
    print(cmdsetip)
    #cmdsetip = 'pipework br0 %s %s/24@192.168.153.1' %(dockerid,containerip)
    stdinnet,stdoutnet,stderrnet = sshobject.exec_command(cmdsetip)
    stdoutnet = stdoutnet.read().decode()
    cmdstartssh = 'docker exec -d %s /root/startssh.sh' %(dockerid)
    stdinssh,stdoutssh,stderrssh = sshobject.exec_command(cmdstartssh)
    stdoutssh = stdoutssh.read().decode()
    cmdchagepw = 'docker exec -d %s /root/cpasswd.sh %s' %(dockerid,password)
    stdincp,stdoutcp,stderrcp = sshobject.exec_command(cmdchagepw)
    stdoutcp = stdoutcp.read().decode()
    #print(stdoutnet.read().decode())
    return stdoutrestart
def stopContainer(sshobject,dockerid):
    cmdstop = 'docker stop %s' % (dockerid)
    stdinstop,stdoutstop,stderrstop = sshobject.exec_command(cmdstop)
    stopresult = stdoutstop.read().decode()
    print(stopresult)
    return stopresult
    #print(stdoutstop.read().decode())
def deleteContainer(sshobject,dockerid):
    cmdstop = 'docker rm %s' % (dockerid)
    stdinstop,stdoutstop,stderrstop = sshobject.exec_command(cmdstop)
    #print(stdoutstop.read().decode())
    deleteresult = stderrstop.read().decode()
    #print(deleteresult)
    return deleteresult
def commitContainer(sshobject,dockerid,imagename):
    #cmddate = 'date "+%Y%m%d%H%M"'
    #stdindate,stdoutdate,stderrdate = sshobject.exec_command(cmddate)
    #print(stdoutdate.read().decode())
    #cdate = stdoutdate.read().decode()
    #print(cdate)
    cmdcommit = 'docker commit %s %s:5000/%s' % (dockerid,imagedomain,imagename)
    stdincommit,stdoutcommit,stderrcommit = sshobject.exec_command(cmdcommit)
    #print(stdoutcommit.read().decode())
    commitresult = stdoutcommit.read().decode()
    #print(commitresult)
    return commitresult
def pushImage(sshobject,imageid,imagename):
    cmdtag = 'docker tag %s %s:5000/%s' %(imageid,imagedomain,imagename)
    print(cmdtag)
    stdintag,stdouttag,stderrtag = sshobject.exec_command(cmdtag)
    cmdpush = 'docker push %s:5000/%s' % (imagedomain,imagename)
    print(cmdpush)
    stdinpush,stdoutpush,stderrpush = sshobject.exec_command(cmdpush)
    #print(stdoutpush.read().decode())
    pushresult = stdoutpush.read().decode()
    #print(commitresult)
    return pushresult


#createContainer(sshClient('192.168.153.80'),'testwindows','192.168.153.80:5000/centos6.6_bao')
#deleteContainer(sshClient('192.168.153.80'),'824fd90f437b')
#pushImage(sshClient('192.168.153.80'),'824fd90f437b','test')
#ip = '192.168.153.80'
#pwd = '123456'
#sshClient(ip,pwd)

