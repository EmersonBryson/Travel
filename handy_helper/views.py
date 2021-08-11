from django.shortcuts import render, redirect
from . models import User, Job
from django.contrib import messages
import bcrypt, datetime


# Create your views here.
# Login and Registration
def index(request):
    if 'logged_user' in request.session:
        return redirect('/dashboard')
    return render(request, 'index.html')

def dashboard(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['logged_user']),
        'jobs': Job.objects.all()
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    newUser = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['logged_user'] = newUser.id
    return redirect('/dashboard')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['logged_user'] = logged_user.id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

# trips
def display_add_job(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['logged_user']),
    }
    return render(request, 'new_job.html', context)

def add_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/jobs/new')
    else:
        logged_user = User.objects.get(id=request.session['logged_user'])
        newJob = Job.objects.create(
            user= logged_user,
            title= request.POST['title'],
            description= request.POST['description'],
            location = request.POST['location'],
        )
    return redirect('/dashboard')

def destroy_job(request, job_id):
    job_to_delete = Job.objects.get(id=job_id)
    user = User.objects.get(id=request.session['logged_user'])
    if user == job_to_delete.user:
        job_to_delete.delete()
    return redirect('/dashboard')

def display_one_job(request, job_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['logged_user']),
        'this_job': Job.objects.get(id=job_id)
    }
    return render(request, 'view_job.html', context)

def display_edit_job(request, job_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    context ={
        'user': User.objects.get(id=request.session['logged_user']),
        'this_job': Job.objects.get(id=job_id)
    }
    return render(request, 'edit_job.html', context)

def update_job(request, job_id):
    if request.method == 'GET':
        return redirect('/dashboard')
    job_to_update = Job.objects.get(id=job_id)
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/jobs/edit/{job_id}')
    else:
        job_to_update.title = request.POST['title']
        job_to_update.description = request.POST['description']
        job_to_update.location = request.POST['location']
        job_to_update.save()
    return redirect('/dashboard')