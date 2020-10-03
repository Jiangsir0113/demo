from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from student.models import User, Student


# Create your views here.

# def login_required(view_func):
#     """登录判断装饰器"""
#
#     def wrapper(request, *view_args, **view_kwargs):
#         # 判断用户是否登录
#         if request.session.has_key("is_login"):
#             # 用户已登录，调用对应的视图
#             return view_func(request, *view_args, **view_kwargs)
#         else:
#             # 用户未登录，跳转到登录页
#             return redirect("/student/login/")

def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        if request.COOKIES.get('username') is None:
            request.COOKIES["username"] = ''
        data = request.COOKIES.get("username")
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        # username = request.GET.get('username')
        # password = request.GET.get('password')
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_check = request.POST.get('check')
        valid_code = request.POST.get('valid_code')
        # print(is_check)
        result = User.objects.filter(username=username, password=password)  # QuerySet
        if valid_code != request.session["valid_code"]:
            return render(request, 'login.html', {"rename": '验证码错误'})
        if len(result) == 1:
            print('校验成功')
            request.session["is_login"] = True
            is_login = request.session["is_login"]
            request.session["username"] = username
            if is_check:
                """当点击记住用户名的时候"""
                request_obj = render(request, 'index.html', {"username": username, "is_login": is_login})
                request_obj.set_cookie("username", username)
                return request_obj
            else:
                """当没点击记住用户名的时候"""
                # obj = HttpResponse("")
                # obj.set_cookie({"username": username, "password": password})
                return render(request, 'index.html', {"username": username, "is_login": is_login})
        else:
            return render(request, 'login.html', {"rename": '用户名密码或错误'})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.getlist('password')
        if password[0] == password[1]:
            User.objects.create(username=username, password=password[0])
            return render(request, 'login.html', {"username": username})
        else:
            return render(request, 'register.html', {'info': '两次密码输入不一致，请重新输入'})


def student(request):
    request.session["is_login"] = True
    is_login = request.session["is_login"]
    stu_obj = Student.objects.all()
    return render(request, 'student.html', locals())


def update(request):
    stu_id = request.POST.get("stu_id")
    stu_name = request.POST.get("stu_name")
    stu_sex = request.POST.get("stu_sex")
    stu_age = request.POST.get("stu_age")
    stu_phone = request.POST.get("stu_phone")
    try:
        Student.objects.filter(id=stu_id).update(name=stu_name, sex=stu_sex, age=stu_age, phone=stu_phone)
        ret = {'msg': 1}
    except:
        ret = {'msg': 0}
    return JsonResponse(ret)


def delete(request, stu_id):
    Student.objects.get(id=stu_id).delete()
    return redirect('/student/student/')


def delete2(request):
    print(request.is_ajax())
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        try:
            Student.objects.get(id=stu_id).delete()
        except:
            ret = {'msg': 0}
        else:
            ret = {'msg': 1}
        return JsonResponse(ret)


def pwd_change(request, name):
    if request.method == 'GET':
        return render(request, 'pwd_change.html')
    elif request.method == 'POST':
        user = User.objects.get(username=name)
        old_pwd = request.POST.get("old_pwd")
        print(old_pwd)
        print(user.password)
        new_pwd = request.POST.getlist('new_pwd')
        if old_pwd != user.password:
            return render(request, 'pwd_change.html', {'info': '旧密码输入错误，请重新输入'})
        elif new_pwd[0] == new_pwd[1]:
            user.password = new_pwd[0]
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'pwd_change.html', {'info': '两次新密码输入不一致，请重新输入'})


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get("add_stu_name")
        sex = request.POST.get("add_stu_sex")
        age = request.POST.get("add_stu_age")
        phone = request.POST.get("add_stu_phone")
        Student.objects.create(name=name, sex=sex, age=age, phone=phone)
        return redirect("/student/student/")


def select_user(request, username):
    request.session["is_login"] = True
    is_login = request.session["is_login"]
    userid = User.objects.get(username=username).id
    name = username
    print(userid, name)
    return render(request, 'select_user.html', locals())


def logout(request):
    request.session['is_login'] = None
    request.session['username'] = None
    return redirect('/student/login/')


# def get_valid_img(request):
#     from PIL import Image, ImageDraw, ImageFont
#     import random
#
#     def get_random_color():
#         return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
#
#     # 生成一个图片对象
#     img_obj = Image.new('RGB', (220, 35), get_random_color())
#
#     # 在生成的图片上写字符
#     # 生成一个画笔对象
#     draw_obj = ImageDraw.Draw(img_obj)
#
#     # 加载字体文件，得到一个字体对象
#     font_obj = ImageFont.truetype("/static/fonts/constan.otf", 28)
#
#     # 开始生成随机字符串并且写到图片上
#     tmp_list = []
#     for i in range(5):
#         u = chr(random.randint(65, 90))
#         l = chr(random.randint(97, 122))
#         n = chr(random.randint(0, 9))
#
#         tmp = random.choice([u, l, n])
#         tmp_list.append(tmp)
#         draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)
#
#     print("".join(tmp_list))
#     print("生成的验证码".center(120, "="))
#
#     # 保存到session中
#     request.session["valid_code"] = "".join(tmp_list)
#
#     from io import BytesIO
#     io_obj = BytesIO()
#
#     # 将生成的图片数据保存在io对象中
#     img_obj.save(io_obj, "png")
#
#     # 从io对象中取出上一步保存的数据
#     data = io_obj.getvalue()
#     return HttpResponse(data)

def get_valid_img(request):
    from captcha.image import ImageCaptcha
    from random import randint
    lst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']
    chars = ''
    for i in range(4):
        chars += lst[randint(0, 36)]
    request.session['valid_code'] = chars
    image = ImageCaptcha(width=80, height=35, font_sizes=(35, 35, 35)).generate_image(chars)
    from io import BytesIO
    io_obj = BytesIO()

    # 将生成的图片数据保存在io对象中
    image.save(io_obj, "png")
    data = io_obj.getvalue()
    return HttpResponse(data)


def index1(request):
    return HttpResponse(111)
 