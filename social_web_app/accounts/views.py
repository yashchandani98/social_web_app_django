
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.generic import View, CreateView
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
# from datetime import datetime, timedelta
from rest_framework.views import APIView
from .models import User

from .forms import RegisterForm, LoginForm

User = get_user_model()


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
      return redirect(reverse('pages:dashboard-view'))
      # return redirect('/home/dashboard/')
      # return render(request, "pages/dashboard.html", self.context)
    self.context['title'] = 'Login'
    self.context['form'] = form
    return render(request, self.template_name, self.context)


class LogoutView(View):
  def get(self, request, *args, **kwargs):
    logout(request)
    messages.success(request, 'You has been logged out successfully!')
    return redirect(reverse('accounts:accounts-login'))


  # class PlayerSignUp(APIView):
  #   def post(self, request):
  #       final_data = []
  #       for player in request.data['data']:

  #         password = base64.b64encode(bytes(player['password'], 'utf-8'))
  #         password = str(password, 'utf-8')
  #         add_players_details = ClubPlayers(name=player['name'],
  #                                           emailId=player['emailId'],
  #                                           username=player['username'],
  #                                           password=password,
  #                                           clubAccessList=player['clubId'],
  #                                           clubMembershipId=clubMemberShipId,
  #                                           phoneNumber=player['mobileNumberCode'] + player['mobileNumber'],
  #                                           profileImage=profileImage,
  #                                           deviceName=player['deviceName'],
  #                                           deviceOs=player['deviceOs'],
  #                                           deviceId=player['deviceId'],
  #                                           deviceType=player['deviceType'],
  #                                           appVersion=player['appVersion'],
  #                                           statusString="Active",
  #                                           phoneNumberCode=player['mobileNumberCode'],
  #                                           employeeTypeCode=player['employeeTypeCode'],
  #                                           status=0,
  #                                           createdOn=datetime.now().timestamp(),
  #                                           showOnLeaderBoard=0,
  #                                           FCMTopic=player['mobileNumber'])


  #         add_players_details.save()
              
  #             response_message = {
  #                 "message": "Success",
  #             }
  #             return JsonResponse(response_message, safe=False, status=200)
  #         else:
  #             response_message = {
  #                 "message": "Bad Request",
  #                 "result": []
  #             }
  #             return JsonResponse(response_message, safe=False, status=400)
