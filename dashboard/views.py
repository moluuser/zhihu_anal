import hashlib

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.core.cache import cache
from django.shortcuts import render, redirect

# Create your views here.
from dashboard.models import User, ZhihuUser, ZhihuQue, ZhihuTag


def dashboard(request):
    if request.session.get('username') is not None:
        return render(request, 'dashboard/dashboard.html')
    else:
        return redirect('login')


def useranal(request):
    if request.session.get('username') is not None:
        return render(request, 'dashboard/useranal.html')
    else:
        return redirect('login')


def contentanal(request):
    if request.session.get('username') is not None:
        return render(request, 'dashboard/contentanal.html')
    else:
        return redirect('login')


def search(request):
    if request.session.get('username') is not None:
        if request.method == 'POST':
            keyword = request.POST.get("keyword", None)
            result = ZhihuQue.objects.filter(title__contains=keyword)[:2000]
            return render(request, 'dashboard/search.html',
                          {'result': result, 'keyword': keyword, 'cnt': result.count()})
        else:
            return render(request, 'dashboard/search.html')
    else:
        return redirect('login')


def zhihuque(request):
    if request.session.get('username') is not None:
        # 每次随机取200条记录
        zhihuques = ZhihuQue.objects.order_by('?')[:100]
        return render(request, 'dashboard/zhihuque.html', {'zhihuques': zhihuques})
    else:
        return redirect('login')


def zhihuuser(request):
    if request.session.get('username') is not None:
        zhihuusers = ZhihuUser.objects.order_by('?')[:100]
        return render(request, 'dashboard/zhihuuser.html', {'zhihuusers': zhihuusers})
    else:
        return redirect('login')


def zhihutag(request):
    if request.session.get('username') is not None:
        zhihutags = ZhihuTag.objects.order_by('?')[:100]
        return render(request, 'dashboard/zhihutag.html', {'zhihutags': zhihutags})
    else:
        return redirect('login')


def users(request):
    if request.session.get('username') is not None:
        users = User.objects.all()
        return render(request, 'dashboard/users.html', {'users': users})
    else:
        return redirect('login')


def statement(request):
    pass
    return render(request, 'dashboard/statement.html')


def register(request):
    if request.method == 'POST':
        capt = request.POST.get("captcha", None)
        key = request.POST.get("hashkey", None)
        if jarge_captcha(capt, key):
            username = request.POST.get('username')
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            if password == repassword:
                # 判断用户名重复
                if User.objects.filter(username=username).first():
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    captcha = {'hashkey': hashkey, 'image_url': image_url}
                    return render(request, 'dashboard/register.html', {'msg': '用户名已存在！', "captcha": captcha})
                else:
                    # 注册
                    user = User()
                    user.username = username
                    user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    user.save()
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    captcha = {'hashkey': hashkey, 'image_url': image_url}
                    return render(request, 'dashboard/register.html', {'msg': '注册成功！', "captcha": captcha})
            else:
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                captcha = {'hashkey': hashkey, 'image_url': image_url}
                return render(request, 'dashboard/register.html', {'msg': '两次密码不一致！', "captcha": captcha})
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            captcha = {'hashkey': hashkey, 'image_url': image_url}
            return render(request, 'dashboard/register.html', {'msg': '验证码错误！', "captcha": captcha})
    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, 'dashboard/register.html', {"captcha": captcha})


def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
        return False


def login(request):
    if request.method == 'POST':
        capt = request.POST.get("captcha", None)
        key = request.POST.get("hashkey", None)
        if jarge_captcha(capt, key):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username).first()
            if user:
                if user.password == hashlib.sha256(password.encode('utf-8')).hexdigest():
                    # 登陆成功
                    request.session['username'] = user.username
                    request.session['usersum'] = User.objects.count()
                    return render(request, 'dashboard/dashboard.html')
                else:
                    hashkey = CaptchaStore.generate_key()
                    image_url = captcha_image_url(hashkey)
                    captcha = {'hashkey': hashkey, 'image_url': image_url}
                    return render(request, 'dashboard/login.html', {'msg': '用户名或密码错误！', "captcha": captcha})
            else:
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                captcha = {'hashkey': hashkey, 'image_url': image_url}
                return render(request, 'dashboard/login.html', {'msg': '用户名或密码错误！', "captcha": captcha})
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            captcha = {'hashkey': hashkey, 'image_url': image_url}
            return render(request, 'dashboard/login.html', {'msg': '验证码错误！', "captcha": captcha})
    else:
        if request.session.get('username') is not None:
            return render(request, 'dashboard/dashboard.html')
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, 'dashboard/login.html', {"captcha": captcha})


def logout(request):
    if request.session.get('username') is not None:
        request.session.flush()
    return redirect('login')


def edit(request):
    if request.session.get('username') is not None:
        if request.method == 'POST':
            username = request.POST.get("username", None)
            pwd = request.POST.get("pwd", None)
            repwd = request.POST.get("repwd", None)
            user = User.objects.get(username=username)
            if username == 'admin':
                return render(request, 'dashboard/edit.html', {'msg': '该用户不允许被修改！', 'user': user})
            elif username != request.session.get('username'):
                return render(request, 'dashboard/edit.html', {'msg': '只允许修改当前用户密码！', 'user': user})
            elif pwd == repwd:
                user.password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                user.save()
                return render(request, 'dashboard/edit.html', {'msg': '修改成功！', 'user': user})
            else:
                return render(request, 'dashboard/edit.html', {'msg': '两次密码不一致！', 'user': user})
        else:
            username = request.GET.get('username')
            user = User.objects.get(username=username)
            return render(request, 'dashboard/edit.html', {'user': user})
    return redirect('login')


def delete(request):
    if request.session.get('username') is not None:
        username = request.GET.get('username')
        user = User.objects.filter(username=username).first()
        # 判断用户存在
        if user:
            if username == 'admin':
                # return redirect(users)
                return render(request, 'dashboard/users.html', {'msg': '不允许删除该用户！'})
            elif username == request.session.get('username'):
                user = User.objects.get(username=username)
                user.delete()
                # return redirect(users)
                return render(request, 'dashboard/users.html', {'msg': '删除成功！'})
            else:
                return render(request, 'dashboard/users.html', {'msg': '只允许删除当前登录用户！'})
        else:
            return redirect('login')
    return redirect('login')
