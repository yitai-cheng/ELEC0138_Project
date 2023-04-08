from django.shortcuts import render
from mysite import models
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Staff,LoginCredential
from django.db.models import Q,Sum
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,get_user_model
from django.http import HttpResponseRedirect
from .utils import send_verification_code, generate_verification_code,check_verification_code
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import rsa
import base64
from .utils import generate_RSA_keys, encrypt_RSA, decrypt_RSA
PAGINATOR_NUMBER = 5
def confirm(request):
    if request.POST.get('username') and request.POST.get('password'):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            return HttpResponseRedirect('/verify?username={}&password={}'.format(
            username,
            password
        ))
        else:
            user = User.objects.create_user(username, '', password)
            user.save()
            login_credential = LoginCredential(username=username, password=password)
            login_credential.save()
            # Log in the new user
            login(request, user)
            return HttpResponseRedirect('/verify?username={}&password={}'.format(
            username,
            password
        ))
            
    return render(request, 'login.html')


def verify(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == request.session.get('verification_code'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                print("准备登录")
                login(request, user)
                return redirect('/staff_list/')
            else:
                print("报错了")
                messages.error(request, 'Username or password is incorrect.')
        elif verification_code:
            print("没有post请求？")
            messages.error(request, 'Verification code is incorrect.')
    return render(request, 'verify.html')
"""def logins(request):
    msg_username = ""
    msg_password = ""
    msg_auth = ""
    is_first_load = True
    is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    print("你他妈有在运行吗")
    if request.method == 'POST':
        if 'verification_code' in request.POST:  # 验证码登录
            verification_code = request.POST.get('verification_code')
            if verification_code == request.session.get('verification_code'):
                username = request.session.get('username')
                password = request.session.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/success/')
                else:
                    msg_auth = "username or password is wrong"
            else:
                msg_auth = "verification code is invalid"
        else:  # 用户名密码登录
            username = request.session.get('username')
            password = request.session.get('password')
            user = authenticate(request, username=username, password=password)
            is_first_load = False
            if user:
                request.session['username'] = username
                request.session['password'] = password
                request.session['verification_code'] = generate_verification_code()
                send_verification_code(user.phone_number, request.session['verification_code'])
                return redirect('/verify_code/')
            else:
                if not username:
                    msg_username = "username is empty"
                if not password:
                    msg_password = "password is empty"
                if username and password:
                    msg_auth = "username or password is wrong"
        if is_ajax_request:
            if user:
                response_data = {'status': 'success'}
            else:
                response_data = {
                    'status': 'failure',
                    'msg_username': msg_username,
                    'msg_password': msg_password,
                    'msg_auth': msg_auth
                }
            return JsonResponse(response_data)
        else:
            return render(request, 'login.html', {'msg_username': msg_username, 'msg_password': msg_password, 'msg_auth': msg_auth, 'is_first_load': is_first_load})

    return render(request, 'login.html', {'is_first_load': is_first_load})
"""
@csrf_exempt
def check_credentials(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            request.session['username'] = username
            request.session['password'] = password
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'})
    else:
        return JsonResponse({'status': 'failure'})
def verify_code_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        request.session['phone_number'] = phone_number
        return redirect('/get_verification_code/')

    return render(request, 'verify_code.html')


def get_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        print(phone_number)
        verification_code = generate_verification_code()
        send_verification_code(phone_number, verification_code)
        request.session['verification_code'] = verification_code
        return JsonResponse({'status': 'success'})

    return render(request, 'get_verification_code.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            msg = "Username already exists"
            return render(request, 'register.html', {'msg': msg})
        if password != password2:
            msg = "password is not same"
            return render(request, 'register.html', {'msg': msg})
        elif username =='' :
            msg = "username is empty"
            return render(request, 'register.html', {'msg': msg})
        elif password == '':
            msg = "password is empty"
            return render(request, 'register.html', {'msg': msg})
        elif email == '':
            msg = "email is empty"
            return render(request, 'register.html', {'msg': msg})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('logins')
    return render(request, 'register.html')
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Staff

class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_list'
    paginate_by = 10

class StaffCreateView(CreateView):
    model = Staff
    template_name = 'staff_create.html'
    fields = ('staff_id', 'name', 'department', 'title', 'gender', 'email','description', 'entry_time', 'salary', 'updated_by')
    success_url = reverse_lazy('staff_list')

class StaffUpdateView(UpdateView):
    model = Staff
    fields = ['staff_id', 'name', 'department', 'title', 'gender', 'description', 'entry_time', 'salary']
    template_name = 'staff_update.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        return super().form_valid(form)

class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'staff_delete.html'
    success_url = reverse_lazy('staff_list')