
from django.urls import path,re_path
from .views import (ProfileListView,ProfileDetailView,AllProfileListView,RemoveFriend,AddFriend,AcceptFriend,RejectFriend)

app_name = 'friends'
urlpatterns = [
    path(
        '',
        ProfileListView.as_view(),
        name='profiles-list'
    ),
    path(
        '<int:id>/detail/',
        ProfileDetailView.as_view(),
        name='profiles-detail'
    ),
    path(
        'explore-friends/',
        AllProfileListView.as_view(),
        name='explore-friends'
    ),
    re_path(
        r'^removeFriend/$',
        RemoveFriend.as_view(),
        name='removeFriend'
    ),
    re_path(
        r'^addfriend/$',
        AddFriend.as_view(),
        name='addfriend'
    ),
    re_path(
        r'^acceptfriend/$',
        AcceptFriend.as_view(),
        name='acceptfriend'
    ),
    re_path(
        r'^rejectfriend/$',
        RejectFriend.as_view(),
        name='rejectfriend'
    )#,
    # path(
    #     '<int:id>/update/',
    #     ProfileUpdateView.as_view(),
    #     name='profiles-update'
    # )
]
