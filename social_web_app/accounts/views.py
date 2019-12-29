
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.generic import View, CreateView
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
# from datetime import datetime, timedelta
from rest_framework.views import APIView
from .models import User
from friends.models import Friends

from .forms import RegisterForm, LoginForm

# User = get_user_model()


# REGISTRATION VIEW
class RegisterView(CreateView):
  model = User
  form_class = RegisterForm
  template_name = 'accounts/register.html'
  success_url = '/accounts/login'

  def form_valid(self, form):
    messages.success(self.request, 'User has been registered successfully!')
    return super(RegisterView, self).form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(RegisterView, self).get_context_data(**kwargs)
    context['title'] = 'Register'
    return context


# LOGIN VIEW
class LoginView(View):
  form = LoginForm
  template_name = 'accounts/login.html'
  context = {}

  def get(self, request, *args, **kwargs):
    form = self.form()
    self.context['title'] = 'Login'
    self.context['form'] = form
    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    form = self.form(request.POST)

    if form.is_valid():
      user = form.cleaned_data.get('user_obj')
      request.session['name'] = user.name
      request.session['id'] = user.id
      request.session['email'] = user.email
      request.session['number'] = user.number
      print(request.session['name'])
      messages.success(request, 'Yay! You just logged in!')
      return redirect(reverse('posts:posts-list'))
      # return redirect('/home/dashboard/')
      # return render(request, "pages/dashboard.html", self.context)
    self.context['title'] = 'Login'
    self.context['form'] = form
    return render(request, self.template_name, self.context)

class ProfileView(View):
  def get(self,request,*args,**kwargs):
    friends = Friends.objects.filter(Q(received_user=request.GET.get('profileId')) | Q(requested_user=request.GET.get('profileId')),active=True)
    print(friends)
    raise SystemExit
    flag=0
    if len(myFriends) == 0:
      myFriends = Friends.objects.filter(requested_user=request.session.get('id'),active=True)
      flag=1
    myProfile = User.objects.get(id=request.session.get('id'))
    friends = list()
    for friend in myFriends:
      if flag==0:
        friendDetails = User.objects.get(id=friend.requested_user)
      else:
        friendDetails = User.objects.get(id=friend.received_user)
      friends.append({"id":friendDetails.id,"name":friendDetails.name,'requestId':friend.id})
    return render(request,'pages/myProfile.html',{"myFriends":friends,"totalFriends":len(myFriends),"myProfile":myProfile,"is_my_profile":0})

class LogoutView(View):
  def get(self, request, *args, **kwargs):
    del request.session['id']
    del request.session['name']
    logout(request)
    messages.success(request, 'You has been logged out successfully!')
    return redirect(reverse('accounts:accounts-login'))

class MyProfileView(View):
  def get(self,request,*args,**kwargs):
    myFriends = Friends.objects.filter(received_user=request.session.get('id'),active=True)
    flag=0
    if len(myFriends) == 0:
      myFriends = Friends.objects.filter(requested_user=request.session.get('id'),active=True)
      flag=1
    myProfile = User.objects.get(id=request.session.get('id'))
    friends = list()
    for friend in myFriends:
      if flag==0:
        friendDetails = User.objects.get(id=friend.requested_user)
      else:
        friendDetails = User.objects.get(id=friend.received_user)
      friends.append({"id":friendDetails.id,"name":friendDetails.name,'requestId':friend.id})
    return render(request,'pages/myProfile.html',{"myFriends":friends,"totalFriends":len(myFriends),"myProfile":myProfile,"is_my_profile":1})