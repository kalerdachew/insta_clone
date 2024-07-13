from django.urls import path
from .import views
urlpatterns=[
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('profile/',views.profile,name="profile"),
    path('setting/',views.setting,name="setting"),
    path('search/',views.search,name="search"),
    path('setting2/',views.setting2,name='setting2'),
    path('upload/',views.upload,name='upload'),
    path('like/<uuid:post_id>',views.like_post,name='like_post'),
    path('dislike/<uuid:post_id>',views.dislike_post,name='dislike_post'),
    path('follow/<str:username>',views.follow_user,name='follow'),
    path('unfollow/<str:username>',views.unfollow_user,name='unfollow'),
]