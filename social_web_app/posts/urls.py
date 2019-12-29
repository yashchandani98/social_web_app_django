from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    # PostUpdateView,
    # PostDeleteView,
    PostLikeView,
    PostUnLikeView,
    ChangePostPrivacy,
    DeletePost
)


app_name = 'posts'
urlpatterns = [
    path(
        '',
        PostListView.as_view(),
        name='posts-list'
    ),
    # path(
    #     '<int:id>/detail/',
    #     PostDetailView.as_view(),
    #     name='posts-detail'
    # ),
    # path(
    #     '<int:id>/update/',
    #     PostUpdateView.as_view(),
    #     name='posts-update'
    # ),
    # path(
    #     '<int:id>/delete/',
    #     PostDeleteView.as_view(),
    #     name='posts-delete'
    # ),
    path(
        'likePost/',
        PostLikeView.as_view(),
        name='likePost'
    ),
    path(
        'post/unlikePost/',
        PostUnLikeView.as_view(),
        name='unlikePost'
    ),
    path(
        'changePrivacy/',
        ChangePostPrivacy.as_view(),
        name='changePrivacy'
    ),
    path(
        'deletePost/',
        DeletePost.as_view(),
        name='deletePost'
    )
]