from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from datetime import datetime
import requests
from .models import *

buyTable = None
sellTable = None


class Register(View):
    template = 'trading/register.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        try:
            # add_company("")
            g = Global.objects.get(pk=1)
            print(g.registrationKey)
            if request.POST["password"] == g.registrationKey:
                user = User.objects.create_user(
                    username=request.POST["username"])
                password = User.objects.make_random_password(length=6)
                user.set_password(password)
                user.save()

                profile = Profile.objects.create(user=user)
                profile.save()
                return render(request, self.template, {"pass": password})
            return render(request, self.template,
                          {"error": "Invalid Registration"})
        except IntegrityError:
            return render(request, self.template,
                          {"error": "Invalid Registration"})



class Login(View):
    template = 'trading/login.html'
    template1 = 'trading/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('../')
        return render(request, self.template, {})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username == "" or password == "":
            message = "Missing username or password"
            context = {"message": message}
            return render(request, self.template, context)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                print()
                print("User in DB")
                print()
                login(request, user)
                return redirect("../")
        else:
            # message = "Invalid Username or Password!"
            # context = {"message": message}
            # return render(request, self.template, context)
            # print()
            # print("User not in DB")
            # print()
            # newuser = requestUser(username, password)
            # if newuser["allow"]:
            #     createUser(newuser)
            #     user = authenticate(username=username, password=password)
            #     login(request, user)
            #     return redirect("../")
            # else:
            message = "Invalid Username or Password!"
            context = {"message": message}
            return render(request, self.template, context)


def Logoff(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("../login")

