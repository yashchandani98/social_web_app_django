
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, UpdateView, DeleteView

from .models import Post
from friends.models import Friends
from accounts.models import User
from likes.models import Like
from .forms import PostForm

from datetime import datetime
# from dateutil import tz

# POST LIST VIEW
class PostListView(View):
  model = Post
  form = PostForm
  template_name = 'posts/post_list.html'
  context = {}

  def get(self, request, *args, **kwargs):
    qs = self.model.objects.filter(active=True).order_by('-created_at')
    posts=list()
    for a in qs:
      print("Privacy:",a.privacy)
      postId = a.id
      ownerId = a.owner_id
      date = datetime.strptime(a.created_at.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
      time = datetime.strptime(a.created_at.strftime('%H:%M'), '%H:%M').time()
      totalLikes = Like.objects.filter(post_id=postId).count()
      is_liked = Like.objects.filter(owner_id=request.session['id'],post_id=postId).count()
      print("is_liked",is_liked)
      print("totalLikes",totalLikes)
      print(int(ownerId)==int(request.session['id']))
      if int(ownerId) == int(request.session['id']):
        owner_details = User.objects.get(id=request.session['id'])
        posts.append({"post":a,"owner":owner_details,"ownerId":int(a.owner_id),"totalLikes":totalLikes,"date":date,"time":time,"is_liked":is_liked,"sessionId":int(request.session['id'])})
      else:
        is_friend = Friends.objects.filter(active=True,requested_user=int(ownerId),received_user=int(request.session['id'])).count()
        if is_friend==0:
          is_friend = Friends.objects.filter(active=True,received_user=int(ownerId),requested_user=int(request.session['id'])).count()
        print("ownerId",int(request.session['id']))
        print("is_friend",is_friend)
        # raise SystemExit
        if is_friend != 0:
          owner_details = User.objects.get(id=a.owner_id)
          posts.append({"post":a,"owner":owner_details,"ownerId":int(a.owner_id),"totalLikes":totalLikes,"date":date,"time":time,"is_liked":is_liked,"sessionId":int(request.session['id'])})
          # print(a.owner_id)
    # raise SystemExit
    form = self.form()
    self.context['title'] = 'Posts'
    self.context['posts'] = posts
    self.context['countPosts'] = len(posts)
    self.context['form'] = form
    return render(request, self.template_name, self.context)

  def post(self, request, *args, **kwargs):
    form = self.form(request.POST)
    if form.is_valid():
      # instance = form.save(commit=False)
      # instance.owner = self.request.session['id']
      # instance.save()
      model = Post(description=request.POST.get('description'),owner_id=request.session['id'],image='')
      model.save()
      messages.success(request, 'Post has been added to feed!')
      return redirect('posts:posts-list')
    messages.error(request, 'Oop! Enter valid details!')
    return reverse('posts:posts-list')

class PostLikeView(View):
  def get(self, request, *args, **kwargs):
    Like(owner_id=request.session['id'],post_id=request.GET.get('id')).save()
    return redirect(reverse('posts:posts-list'))

class PostUnLikeView(View):
  def get(self, request, *args, **kwargs):
    Like.objects.filter(owner_id=request.session['id'],post_id=request.GET.get('id')).delete()
    return redirect(reverse('posts:posts-list'))


# POST DETAIL VIEW
class PostDetailView(DetailView):
  queryset = Post.objects.all()
  context_object_name = 'post'
  lookup = 'id'
  
  def get_object(self, *args, **kwargs):
    return get_object_or_404(Post, pk=self.kwargs.get(self.lookup))
  
  def get_context_data(self, *args, **kwargs):
    context = super(PostDetailView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Post Detail'
    return context


# POST UPDATE VIEW
# class PostUpdateView(LoginRequiredMixin, UpdateView):
#   queryset = Post.objects.all()
#   form_class = PostForm
#   context_object_name = 'post'
#   template_name = 'posts/post_update.html'
#   lookup = 'id'

#   def get_object(self, *args, **kwargs):
#     return Post.objects.get_user_post(
#       self.kwargs.get(self.lookup),
#       self.request.user
#     )

#   def get_context_data(self, *args, **kwargs):
#     context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
#     context['title'] = 'Post Update'
#     return context
  
#   def get_success_url(self, *args, **kwargs):
#     messages.success(self.request, 'Post has been updated successfully!')
#     return reverse('posts:posts-detail', kwargs={'id': self.kwargs.get(self.lookup)})


# # POST DELETE VIEW
# class PostDeleteView(LoginRequiredMixin, DeleteView):
  queryset = Post.objects.all()
  context_object_name = 'post'
  template_name = 'posts/post_delete.html'
  lookup = 'id'

  def get_object(self, *args, **kwargs):
    return Post.objects.get_user_post(
      self.kwargs.get(self.lookup),
      self.request.user
    )
  
  def get_context_data(self, *args, **kwargs):
    context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Post Delete'
    return context

  def get_success_url(self, *args, **kwargs):
    messages.success(self.request, 'Post has been deleted!')
    return reverse('posts:posts-list')

class ChangePostPrivacy(View):
  def get(self,request,*args,**kwargs):
    if int(request.GET.get('privacy')) == 1:
      setPrivacy=True
    else:
      setPrivacy=False
    Post.objects.filter(id=int(request.GET.get('id'))).update(privacy=setPrivacy)
    return redirect(reverse('posts:posts-list'))
class DeletePost(View):
  def get(self,request,*args,**kwargs):
        Post.objects.filter(id=int(request.GET.get('id'))).update(active=False)
        return redirect(reverse('posts:posts-list'))