
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

urlpatterns = [
    re_path(
        r'home/',
        include('pages.urls',namespace='pages')
    ),
    # path(
    #     'dev/',
    #     include('pages.urls', namespace='pages')
    # ),
    path(
        'accounts/',
        include('accounts.urls', namespace='accounts')
    ),
    path(
        'posts/',
        include('posts.urls', namespace='posts')
    ),
    path(
        'posts/',
        include('likes.urls', namespace='likes')
    ),
    path(
        'friends/',
        include('friends.urls', namespace='profiles')
    ),
    path('admin/', admin.site.urls),
]