from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Staff

PAGINATOR_NUMBER = 5


def logins(request):
    msg_username = ""
    msg_password = ""
    msg_auth = ""
    is_first_load = True
    is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        is_first_load = False

        # Check if the username and password are provided
        if username and password:
            # INSECURE: Raw SQL query with string formatting - vulnerable to SQL injection
            user = User.objects.raw(
                f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'")

            # Check if the query returned a user
            try:
                user = next(iter(user))
            except StopIteration:
                user = None
                msg_auth = "Username or password is wrong"
        else:
            if not username:
                msg_username = "Username is empty"
            if not password:
                msg_password = "Password is empty"

        if user is not None:
            login(request, user)
            return redirect('/staff_list/')

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
        return render(request, 'login.html',
                      {'msg_username': msg_username, 'msg_password': msg_password, 'msg_auth': msg_auth,
                       'is_first_load': is_first_load})


# def logins(request):
#     msg_username = ""
#     msg_password = ""
#     msg_auth = ""
#     is_first_load = True
#     is_ajax_request = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         is_first_load = False
#
#         if user is not None:
#             login(request, user)
#             return redirect('/staff_list/')
#         else:
#             if not username:
#                 msg_username = "Username is empty"
#             if not password:
#                 msg_password = "Password is empty"
#             if username and password:
#                 msg_auth = "Username or password is wrong"
#
#     if is_ajax_request:
#         if user:
#             response_data = {'status': 'success'}
#         else:
#             response_data = {
#                 'status': 'failure',
#                 'msg_username': msg_username,
#                 'msg_password': msg_password,
#                 'msg_auth': msg_auth
#             }
#         return JsonResponse(response_data)
#     else:
#         return render(request, 'login.html',
#                       {'msg_username': msg_username, 'msg_password': msg_password, 'msg_auth': msg_auth,
#                        'is_first_load': is_first_load})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # add password generator???
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
        return redirect('logins')
    return render(request, 'register.html')


class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_list'
    paginate_by = 10


class StaffCreateView(CreateView):
    model = Staff
    template_name = 'staff_create.html'
    fields = (
        'staff_id', 'name', 'department', 'title', 'gender', 'email', 'description', 'entry_time', 'salary',
        'updated_by')
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
