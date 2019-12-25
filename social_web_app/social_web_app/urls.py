
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

urlpatterns = [
    re_path(
        r'home/',
        include('pages.urls','pages')
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
        'posts/',
        include('unlikes.urls', namespace='unlikes')
    ),
    path(
        'posts/',
        include('comments.urls', namespace='comments')
    ),
    path(
        'profiles/',
        include('profiles.urls', namespace='profiles')
    ),
    path('admin/', admin.site.urls),
]