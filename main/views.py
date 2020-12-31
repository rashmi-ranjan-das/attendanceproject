from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def registration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        collegeid = request.POST['collegeid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        photo = request.FILES['photo']
        if Student.objects.filter(collegeid=collegeid).exists():
            messages.info(request, "Email ID already exists.")
            return redirect('/register')
        elif password1 != password2:
            messages.info(request, "Password doesn't match.")
            return redirect('/register')
        else:
            student = Student(firstname = firstname, lastname= lastname, collegeid= collegeid, password1=password1, password2= password2, photo = photo)
            student.save()
            messages.info(request, "Registration Successful")
            return redirect('/register')

def register(request):
    return render(request, 'main/register.html')

def login(request):
    if request.method == 'POST':
        collegeid = request.POST['collegeid']
        password = request.POST['password1']
        user = Student.objects.get(collegeid= collegeid)
        if user is not None:
            print(user.id)
            return redirect('/profile/Awukj234&profileid_3_kCJ/'+str(user.id))
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')
    else:
        return render(request, 'main/login.html')

def profile(request, id):
    user = Student.objects.get(id = id)
    print(user.firstname)
    return render(request, 'main/profile.html', {'user':user})

def logout(request):
    return redirect('/')

def recognition(request):
    pass