from django.shortcuts import render
from mysite import models
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Staff
from django.db.models import Q,Sum
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,get_user_model
from django.http import HttpResponseRedirect
from .utils import send_verification_code, generate_verification_code,check_verification_code
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
import json

PAGINATOR_NUMBER = 5
def logins(request):
    msg_username = ""
    msg_password = ""
    msg_auth = ""
    is_first_load = True
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        is_first_load = False
        if user:
            verification_code = generate_verification_code()
            send_verification_code(user.phone_number, verification_code)
            request.session['verification_code'] = verification_code
            return HttpResponseRedirect('/verify_code/')

        else:
            if not username:
                msg_username = "username is empty"
            if not password:
                msg_password = "password is empty"
            if username and password:
                msg_auth = "username or password is wrong"

        return render(request, 'login.html', {'msg_username': msg_username, 'msg_password': msg_password, 'msg_auth': msg_auth,'is_first_load': is_first_load})

    return render(request, 'login.html', {'is_first_load': is_first_load})

def get_verification_code(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        phone_number = body.get('phone_number')
        verification_code = generate_verification_code()
 
        send_verification_code(phone_number, verification_code)
        request.session['verification_code'] = verification_code
        return JsonResponse({'status': 'success'})
        
def verify_code_view(request):
    if request.method == 'POST':
        user_code = request.POST['verification_code']
        phone_number = request.session.get('phone_number')
        if check_verification_code(phone_number, user_code):
            login(request, request.user)
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/verify_code/')

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