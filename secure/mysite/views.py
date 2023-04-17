import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import random
import string
from .utils import send_verification_code, generate_verification_code, check_verification_code
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Staff
PAGINATOR_NUMBER = 5


def generate_password(length):
    """Generate a random password of the specified length."""
    # Define the character set to use for the password
    char_set = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password by choosing a random character from the set
    password = ''.join(random.choice(char_set) for i in range(length))

    return password


def generate_password_view(request):
    # Generate a password of length 10
    password = generate_password(10)

    # Return the password as a JSON response
    return JsonResponse({'password': password})


def confirm(request):
    print("confirm")
    if request.method == 'POST':
        # print(request.POST)
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                request.session['username'] = username
                request.session['password'] = password
                redirect_url = reverse('verify')
                print(redirect_url)
                return redirect(redirect_url)
            else:
                error_message = "Invalid username or password"
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Missing username or password"
            return render(request, 'login.html', {'error_message': error_message})
    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def verify(request):
    print(request)
    if request.method == 'POST':
        email = request.POST.get('phone_number')
        verification_code = request.POST.get('verification_code')
        print(email)
        if check_verification_code(email, verification_code):
            username = request.session.get('username')
            password = request.session.get('password')
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
        verification_code = generate_verification_code()
        print(verification_code)
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
        elif username == '':
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
        return redirect(reverse('confirm'))
    return render(request, 'register.html')


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_list'
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('staff_list')
        else:

            error_message = 'Invalid username or password.'
            return render(request, self.template_name, {'error_message': error_message})


class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    template_name = 'staff_create.html'
    fields = (
        'staff_id', 'name', 'department', 'title', 'gender', 'email', 'description', 'entry_time', 'salary',
        'updated_by')
    success_url = reverse_lazy('staff_list')


class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    fields = ['staff_id', 'name', 'department', 'title', 'gender', 'description', 'entry_time', 'salary']
    template_name = 'staff_update.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.username
        return super().form_valid(form)


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = 'staff_delete.html'
    success_url = reverse_lazy('staff_list')
