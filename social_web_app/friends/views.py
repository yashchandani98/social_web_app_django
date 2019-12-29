
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
  View,
  ListView,
  CreateView,
  DetailView,
  UpdateView,
  DeleteView
)

# from .models import Profile, Education, Experience, Social
from .models import (Friends,FriendRequest)
from accounts.models import User
# from .forms import ProfileForm, EducationForm, ExperienceForm, SocialForm



# PROFILE LIST VIEW
class ProfileListView(ListView):
  queryset = Friends.objects.filter()
  context_object_name = 'profiles'
  template_name = 'friends/profile_list.html'

  # def get_context_data(self, *args, **kwargs):
  #   queryset = Friends.objects.filter()
  #   context = super(ProfileListView, self).get_context_data(*args, **kwargs)
  #   context['title'] = 'Profiles'
  #   return context
  # def get_context_data(self, *args, **kwargs):
  #   queryset = User.objects.filter()
  #   context = super(ProfileListView, self).get_context_data(*args, **kwargs)
  #   context['title'] = 'Profiles'
  #   return context
  def get(self,request,*args, **kwargs):
    queryset = Friends.objects.filter(received_user=request.session.get('id'))
    print("queryset",queryset)
    myFriends = list()
    for friends in queryset:
      requestedUser = User.objects.get(id=friends.requested_user)
      # print(requestedUser.id)
      # requestedUser = User.objects.filter(id=friends.requested_user)
      friendsDetail={'id':requestedUser.id,'name':requestedUser.name}
      myFriends.append(friendsDetail)
      print("queryset",myFriends)
    return render(request, 'friends/profile_list.html', {"title":'My Friends',"profiles":queryset})


class AllProfileListView(ListView):
  queryset = Friends.objects.filter()
  context_object_name = 'profiles'
  template_name = 'profiles/profile_list.html'

  def get(self,request,*args, **kwargs):
    friendRequests = FriendRequest.objects.filter(received_user=request.session.get('id'),active=True)
    totalRequests=list()
    for requests in friendRequests:
      userRequest = User.objects.get(id=requests.requested_user)
      friendsDetail={'id':userRequest.id,'name':userRequest.name,'requested_user':requests.requested_user}
      totalRequests.append(friendsDetail)
    allUsers = User.objects.filter(active=True)
    return render(request, 'friends/profile_list.html', {"title":'Explore Friends',"allUsers":allUsers,"friendRequests":totalRequests,"totalRequests":len(totalRequests)})

class RemoveFriend(View):
  def get(self,request,*args, **kwargs):
    Friends.objects.filter(id=request.GET.get('id')).update(active=False)
    print(request.GET.get('id'))
    return redirect(reverse('accounts:myProfile'))


class AddFriend(View):
  def get(self,request,*args, **kwargs):
    request = FriendRequest(requested_user=request.session['id'],received_user=request.GET.get('id'))
    request.save()
    return redirect(reverse('friends:profiles-list'))

class AcceptFriend(View):
  def get(self,request,*args, **kwargs):
        FriendRequest.objects.filter(requested_user=request.GET.get('id'),received_user=request.session['id']).update(active=False)
        friend_new = Friends(requested_user=request.GET.get('id'),received_user=request.session['id'])
        friend_new.save()
        return redirect(reverse('friends:profiles-list'))

class RejectFriend(View):
  def get(self,request,*args, **kwargs):
        FriendRequest.objects.filter(requested_user=request.GET.get('id'),received_user=request.session['id']).update(active=False)
        # friend_new = Friends(requested_user=request.GET.get('id'),received_user=request.session['id'])
        # friend_new.save()
        return redirect(reverse('friends:profiles-list'))

# PROFILE CREATE VIEW
# class ProfileCreateView(LoginRequiredMixin, CheckAuthProfileMixin, CreateView):
#   queryset = Profile.objects.all()
#   template_name = 'friends/profile_create.html'
#   form_class = ProfileForm

#   def form_valid(self, form):
#     form.instance.user = self.request.user
#     messages.success(self.request, 'Profile has been created successfully!')
#     return super(ProfileCreateView, self).form_valid(form)

#   def get_context_data(self, *args, **kwargs):
#     context = super(ProfileCreateView, self).get_context_data(*args, **kwargs)
    
#     if self.get_object() is None:
#       context['title'] = 'Create Profile'
#       return context
#     else:
#       context['title'] = 'Create Profile'
#       context['profile'] = self.get_object()
#       return context


# # PROFILE DETAIL VIEW
class ProfileDetailView(LoginRequiredMixin, DetailView):
  queryset = Friends.objects.all()
  context_object_name = 'profile'

  def get_object(self, *args, **kwargs):
    return get_object_or_404(
      Profile,
      pk=self.kwargs.get('id')
    )

  def get_context_data(self, *args, **kwargs):
    context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
    context['title'] = self.get_object().name
    return context