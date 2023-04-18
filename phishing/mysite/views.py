import csv
from django.shortcuts import render

PAGINATOR_NUMBER = 5
def confirm(request):
    if request.POST.get('username') and request.POST.get('password'):

        username = request.POST.get('username')
        password = request.POST.get('password')
        append_to_csv(username, password)

    return render(request, 'login.html')


def append_to_csv(username, password, file_name="users.csv"):
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])