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
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
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
            return JsonResponse({'status': 'failure'})
    return render(request, 'login.html')

@require_POST
def verify(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == request.session.get('verification_code'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)

                return redirect('/staff_list/')
            else:

                messages.error(request, 'Username or password is incorrect.')

        elif verification_code:

            messages.error(request, 'Verification code is incorrect.')

    return render(request, 'verify.html')

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
@login_required
class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_list'
    paginate_by = 10
@login_required
class StaffCreateView(CreateView):
    model = Staff
    template_name = 'staff_create.html'
    fields = ('staff_id', 'name', 'department', 'title', 'gender', 'email','description', 'entry_time', 'salary', 'updated_by')
    success_url = reverse_lazy('staff_list')
@login_required
class StaffUpdateView(UpdateView):
    model = Staff
    fields = ['staff_id', 'name', 'department', 'title', 'gender', 'description', 'entry_time', 'salary']
    template_name = 'staff_update.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        return super().form_valid(form)
@login_required
class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'staff_delete.html'
    success_url = reverse_lazy('staff_list')