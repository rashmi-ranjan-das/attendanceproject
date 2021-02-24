from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
import cv2
import face_recognition
import numpy as np
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import os
import face_recognition
from datetime import datetime
import csv

def markattendance(name ,user):
    full_name = user.firstname + ' ' + user.lastname
    print('attendance marked')
    workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in
    c = os.path.join(workpath, 'admin.csv')
    with open(c, 'r+') as f:
        data = f.readlines()
        namelist = []
        for line in data:
            entry = line.split(',')[0]
            namelist.append(entry)
            if name not in namelist:
                now = datetime.now()
                dt_string = now.strftime('%H:%M:%S')
                f.writelines(f'\n{full_name},{dt_string}')
                return {'name': full_name, 'time': dt_string}
    return True



# Create your views here.
def attendance(request ,id):
    user = Student.objects.get(pk = id)
    path = 'media/images'
    images = os.listdir(path)
    imgs = []
    names = []
    for cl in images:
        img = face_recognition.load_image_file(f'{path}/{cl}')
        # print(img)
        imgs.append(img)
        names.append(cl.split('.')[0])
    encodinglist = []
    for enc in imgs:
        enc = cv2.cvtColor(enc, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(enc)[0]
        encodinglist.append(encode)
    capture = cv2.VideoCapture(0)
    while True:
        try:
            success, image = capture.read()
            # print(image)
            imgs = cv2.resize(image, (0, 0), None, 0.25, 0.25)
            imgs = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            facescurrent = face_recognition.face_locations(imgs)
            faceenccurrent = face_recognition.face_encodings(imgs, facescurrent)
        except:
            return render(request, 'main/confirm.html')

        for encode, faceLoc in zip(faceenccurrent, facescurrent):
            compare = face_recognition.compare_faces(encodinglist, encode)
            facedis = face_recognition.face_distance(encodinglist, encode)
            bestindex = np.argmin(facedis)
            if compare[bestindex]:
                name = names[bestindex].upper()
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                value=markattendance(name ,user)
                return render(request,'main/confirm.html', value)
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
            student = Student(firstname=firstname, lastname=lastname, collegeid=collegeid, password1=password1,
                              password2=password2, photo=photo)
            student.save()
            messages.info(request, "Registration Successful")
            return redirect('/register')


def register(request):
    return render(request, 'main/register.html')


def login(request):
    if request.method == 'POST':
        collegeid = request.POST['collegeid']
        password = request.POST['password1']
        user = Student.objects.get(collegeid=collegeid)
        if user is not None:
            print(user.id)
            return redirect('/profile/Awukj234&profileid_3_kCJ/' + str(user.id))
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/login')
    else:
        return render(request, 'main/login.html')


def profile(request, id):
    user = Student.objects.get(id=id)
    print(user.firstname)
    return render(request, 'main/profile.html', {'user': user})


def logout(request):
    return redirect('/')


def recognition(request):
    pass
