from django.shortcuts import render , HttpResponseRedirect
from .forms import SignUpForm , LoginForm , PostForm
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .models import Post
from django.contrib.auth.models import Group
# from django.contrib.auth.decorators import login_required


# Create your views here.

#####home####
def home(request):
    post = Post.objects.all()
    return render(request , 'blog/home.html',{'posts':post})


#####about####
def about(request):
    return render(request , 'blog/about.html')

##### Contact ####
def contact(request):
    return render(request , 'blog/contact.html')

##### DashBoar d####
# @login_required
def dashboard(request):
    if request.user.is_authenticated:
     posts = Post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     gps = user.groups.all()
     perms = user.get_all_permissions()
     return render(request , 'blog/dashboard.html',{'posts':posts , 'full_name':full_name ,'groups':gps , 'perms': perms})
    else:
        return HttpResponseRedirect('/login/')

##### Logout ####
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

##### Signup d####
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request , 'Congratulations !!!!! You have Become an Author')
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
            return render(request, 'blog/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request , 'blog/signup.html' , {'form':form})


##### Login d####
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request , data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname , password=upass)
                if user is not None:
                    login(request , user)
                    messages.success(request , 'Logged in Successfully !!!!!!')
                    return HttpResponseRedirect('/dashboard/')
                
        else:
            form = LoginForm()
        return render(request , 'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

########Add-Post #

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
                return HttpResponseRedirect('/dashboard/')  # Redirect after successful post creation
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
    

# Update Post #

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST , instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request , 'blog/updatepost.html',{'form':form})            
    else:
        return HttpResponseRedirect('/login/')
    


# Udate  Post #
def delete_post(request , id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

    


    