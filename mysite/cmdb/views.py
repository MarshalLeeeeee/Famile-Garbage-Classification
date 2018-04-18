from .family import *
from .collector import *
from .dumpstation import *
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.

user_list = [

]
def index(request):
    #return HttpResponse("hello")
    if request.method == 'POST':
        print('index post')
        username = request.POST.get("username", None)
        #print(username)
        password = request.POST.get("password", None)
        login = familyoperate(username, password, 0, 0, 0)
        # print(login.userName)
        state = login.logIn(username, password)
        if state == 3:
            print('3')
            messages.add_message(request, messages.ERROR, '用户名未注册')
            return render(request, 'index.html')
        elif state == 1:
            print('1')
            messages.add_message(request, messages.ERROR, '密码错误')
            return render(request, 'index.html')
        elif state == 2:
            print("succ")
            # 显示已经投放的垃圾信息
            info = login.garbageinformation()
            # info.replace("0"," ")
            print(info)
            return HttpResponseRedirect('/info?info='+login.userName+'!'+str(login.account)+'!'+login.phonenum+'!'+login.address+'!'+info)

    return render(request, "index.html")
    # return HttpResponseRedirect()

def register(request):
    if request.method == 'POST':
        print('register post')
        user_name = request.POST.get('user_name', None)
        user_address = request.POST.get('user_address', None)
        user_password = request.POST.get('user_password', None)
        user_confirm_password = request.POST.get('user_confirm_password', None)
        user_phone1 = request.POST.get('user_phone1', None)
        if user_password != user_confirm_password:
            messages.add_message(request, messages.ERROR, '密码不一致')
            return render(request, 'register.html')
        else:
            reg = familyoperate(user_name, user_password, 0, user_address, user_phone1)
            state = reg.signup(user_name, user_password, 0, user_address, user_phone1)
            if state == 0:
                messages.add_message(request, messages.ERROR, '用户名或密码不能为空')
                return render(request, 'register.html')
            elif state == 1:
                messages.add_message(request, messages.ERROR, '用户名已被注册')
                return render(request, 'register.html')
            elif state == 2:
                messages.add_message(request, messages.ERROR, '注册成功,请点击按钮返回登录界面')
                return render(request, 'register.html')
    return render(request, 'register.html',)

def show_info(request):
    if request.method == 'POST':
        print('show_info post')
        garbageType = int(request.POST.get('type',None))
        username = request.POST.get('user_name',None)
        drop = Collector(0, 'SJTU')
        drop.currentUsr = username
        drop.state = 1
        state = drop.dumpgarbage(garbageType)
        # data = []
        data = drop.returnUsedSpace()
        print('d')
        print(data)
        if state == -1:
            messages.add_message(request, messages.ERROR, '只有用户才能投放垃圾')
            return render(request, 'show_info.html', {'data1': data[0], 'data2':data[1],'data3':data[2]})
        elif state == 0:
            messages.add_message(request, messages.ERROR, '余额不足，请充值')
            return render(request, 'show_info.html', {'data1': data[0], 'data2':data[1],'data3':data[2]})
        elif state == 1:
            messages.add_message(request, messages.ERROR, '我已经饱了，别再喂我了！')
            return render(request, 'show_info.html', {'data1': data[0], 'data2':data[1],'data3':data[2]})
        else:
            print('succ')
            messages.add_message(request, messages.ERROR, '投放成功!')
            return render(request, 'show_info.html', {'data1': data[0], 'data2':data[1],'data3':data[2]})
    return render(request, 'show_info.html',)

def identify(request):
    if request.method == 'POST':
        print('identify post')
        username = request.POST.get('user_name',None)
        useraddr = request.POST.get('user_address',None)
        userphone = request.POST.get('user_phone',None)
        change = familyoperate(username,0,0,useraddr,userphone)
        change.changeaddress(useraddr)
        change.changephone(userphone)
        messages.add_message(request, messages.ERROR, '修改成功!')
        return render(request, 'identify.html', )
    return render(request, 'identify.html',)

def admin(request):
    if request.method == 'POST':
        print('admin post')
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        garbageType = int(request.POST.get('type', None))
        login = Collector(0,'SJTU')
        state = login.logIn(username,password,garbageType)
        if state == 0:
            messages.add_message(request, messages.ERROR, '用户名错误')
            return render(request, 'admin.html')
        elif state == 1:
            messages.add_message(request, messages.ERROR, '密码错误')
            return render(request, 'admin.html')
        elif garbageType == 3:
            return HttpResponseRedirect('/repair')
        elif garbageType == 2:
            return HttpResponseRedirect('/recycle')

    return render(request, 'admin.html',)
def repair(request):
    # if request.method == 'POST':
        return render(request, 'repair.html')

def recycle(request):
    # if request.method == 'POST':
        return render(request, 'recycle.html')


def station(request):
    #return HttpResponse("hello")
    if request.method == 'POST':
        print('station post')
        username = request.POST.get("username", None)
        #print(username)
        password = request.POST.get("password", None)
        login = DumpStation('SJTU')
        # print(login.userName)
        state = login.dump(username, password)
        if state == 0:
            messages.add_message(request, messages.ERROR, '用户名未注册')
            return render(request, 'station.html')
        elif state == 1:
            # print('1')
            messages.add_message(request, messages.ERROR, '密码错误')
            return render(request, 'station.html')
        else:
            print("succ")
            messages.add_message(request, messages.ERROR, '正在处理...')
            return render(request, 'station.html')

    return render(request, "station.html")
    # return HttpResponseRedirect()