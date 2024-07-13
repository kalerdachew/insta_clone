
from email.mime import image
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,Post,LikePost, follow
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='signin')
def index(request):
  user_object=User.objects.get(username=request.user.username)
  user_profile=Profile.objects.get(user=user_object)
  posts=Post.objects.all()
  current_user=request.user
  follows=follow.objects.all()
  suggested_user=Profile.objects.exclude(id=current_user.id)
  return render(request,'index.html',{'user_profile':user_profile,'posts':posts,'suggested_users':suggested_user,'follows':follows})
def signup(request):
    if request.method=='POST':
      username=request.POST['username']
      email=request.POST['email']
      password=request.POST['password']
      password2=request.POST['password2']
      
      if password==password2:
         if User.objects.filter(email=email).exists():
            messages.info(request,"Email already taken")
            return redirect('signup')
         elif User.objects.filter(username=username).exists():
            messages.info(request,"username already taken")
            return redirect('signup')
         else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #login user and redirect it into settings page
            user_login=auth.authenticate(username=username,password=password)
            auth.login(request,user_login)
             #create profile object for a user
            user_model=User.objects.get(username=username)
            new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)    # type: ignore
            new_profile.save()
            return redirect('setting')
      else:
         messages.info(request,"Password is not Macthing")
         return redirect('signup')
    else:
      return render(request,'signup.html')
def profile(request):
    user_profile=Profile.objects.get(user=request.user)
    user_posted=Post.objects.filter(user=request.user)
    return render(request,'profile.html',{'user_profile':user_profile,'user_posted':user_posted})
def signin(request):
    if request.method == 'POST':
       username=request.POST['username']
       password=request.POST['password']

       user=auth.authenticate(username=username,password=password)

       if user is not None:
          auth.login(request,user)
          return redirect('/')
       else:
          messages.info(request,'invalid credentials')
          return redirect('/signin')
    return render(request,'signin.html')
def search(request):
    return render(request,'search.html')
#logging out
@login_required(login_url='signin')
def logout(request):
   auth.logout(request)
   return redirect(request,'signin')

@login_required(login_url='signin')
def setting(request):
   user_profile=Profile.objects.get(user=request.user)
   if request.method=='POST':
     if request.FILES.get('image') == None:
        image=user_profile.profileimg
        bio=request.POST['bio']
        location=request.POST['location']

        user_profile.profileimg=image # type: ignore
        user_profile.bio=bio
        user_profile.location=location
        user_profile.save()
     if request.FILES.get('image')!=None:
       image=request.FILES.get('image') 
       bio=request.POST['bio']
       location=request.POST['location']

       user_profile.profileimg=image 
       user_profile.bio=bio
       user_profile.location=location
       user_profile.save()
       return redirect('setting')

   return render(request,'setting.html',{'user_profile':user_profile})

##settings test view
def setting2(request):
   uss_now=Profile.objects.get(user=request.user)
   # uss_pro=Profile.objects.all()
   return render(request,'settings2.html',{'uss_pro':uss_now})
@login_required(login_url='signin')
def upload(request):
   
   if request.method=='POST':
      user=request.user.username
      image=request.FILES.get('image_upload')
      caption=request.POST['caption']
      
      newpost=Post.objects.create(user=user,image=image,caption=caption)
      newpost.save() 
      return redirect('/')
   else:
      return redirect('/')
  
@login_required(login_url='/signin')
def like_post(request,post_id):
  post = Post.objects.get(pk=post_id)

  if request.user in post.likes.all():
        post.likes.remove(request.user)
  else:
        post.likes.add(request.user)

  return redirect('/')

@login_required(login_url='/signin')
def dislike_post(request,post_id):
  post = Post.objects.get(pk=post_id)

  if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
  else:
        post.dislikes.add(request.user)

  return redirect('/')

@login_required(login_url='signin')
def follow_user(request,username):
   user_to_follow=get_object_or_404(User,username)
   if request.user != user_to_follow:
      follow.objects.get_or_create(follower=request.user,followed=user_to_follow)
   return redirect('/')
   
@login_required(login_url='signin')
def unfollow_user(request,username):
   user_to_unfollow=get_object_or_404(User,username)
   if request.user != user_to_unfollow:
      follow.objects.filter(follower=request.user,followed=user_to_unfollow).delete()
   return redirect('/')
# Create your views here.
