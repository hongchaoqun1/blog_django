from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, RegistForm
from .models import Userprofile, UserInfo
# Create your views here.

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            user = authenticate(username=cd['username'], password=cd["password"])
            if user:
                login(request, user)
                return HttpResponse("wellcom")
            else:
                return HttpResponse("用户不存在")
        else:
            return HttpResponse("Invalid login")
    if request.method == "GET":
        form = LoginForm()
        return render(request, "account/login.html", {"form":form})

def register(request):
    if request.method == "POST":
        form = RegistForm()
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.clean_data["password"])
            new_user.save()
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry, 注册失败 ")
    else:
        form = RegistForm()
        return render(request, "account/register.html", {"form":form})

def register_pro(request):
    error = ''
    if request.method == "POST":
        data = request.POST
        username = data.get("username", '')
        password = data.get("password", '')
        password2 = data.get("password2", "")
        email = data.get("email", '')
        phone = data.get("phone", '')

        if not username:
            error = "没有提供用户名"
            return HttpResponse(error)

        if User.objects.filter(username=username):
            error = "用户名已存在"
            return HttpResponse(error)
        
        if password != password2:
            error = "密码不一致"
            return HttpResponse(error)
        
        #user = User()
        #user.username = username
        #user.set_password(password)
        #user.email = email
        User.objects.create_user(username=username,password=password)
        user = authenticate(username=username, password=password)
        print(user.password)
        user.email = email
        user_profile = Userprofile()
        user.save()
        user_profile.user = user
        user_profile.phone = phone
        user_profile.save()
        return HttpResponse("注册成功")
    else:
        return render(request, "account/register2.html")    

@login_required(login_url='/auth/login')    
def editInfo(request):
    if request.method == "POST":
        data = request.POST
        school = data.get("school", '')
        company = data.get("company", '')
        profession = data.get("profession", '')
        address = data.get("address", '')
        aboutme = data.get("aboutme", '')

        user = User.objects.filter(username=request.user.username)[0]
        userinfo = UserInfo()
        userinfo.user = user
        userinfo.school = school
        userinfo.company = company
        userinfo.profession = profession
        userinfo.address = address
        userinfo.aboutme = aboutme
        userinfo.save()
        return HttpResponse("上传成功")
    else:
        return render(request, "account/edit_info.html")

@login_required(login_url="/auth/login")
def showInfo(request):
    user = User.objects.filter(username = request.user.username)[0]
    userinfo = {}
    userinfo["username"] = user.username
    userinfo["email"] = user.email
    userinfo["school"] = user.userinfo.school
    userinfo['company'] = user.userinfo.company
    userinfo["profession"] = user.userinfo.profession
    userinfo["address"] = user.userinfo.address
    userinfo["aboutme"] = user.userinfo.aboutme
    print(userinfo)
    return render(request, "account/userinfo.html", userinfo)
