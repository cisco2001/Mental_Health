from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Student
from blog.models import Post

def home(request):
    latest_posts = Post.objects.order_by('-created_on')[:3]
    context = {
        'latest_posts': latest_posts,
    }
    return render(request, "home.html", context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if username and password and email:
            user = Student.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Invalid registration details')
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        # Extract data from the request
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the student
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '')
            if next_url:
                print(next_url)
                return redirect(next_url)
            else:
                return redirect('home')
    
    return render(request, 'login.html', {'next': request.GET.get('next', '')})

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to the home page or any other page

def complete_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            birth_date = request.POST['birth_date']
            course = request.POST['course']
            request.user.birth_date = birth_date
            request.user.course = course
            request.user.save()
            return redirect('home')
        return render(request, 'complete_profile.html')
    else:
        return redirect('login')