from django.db import models
import re, bcrypt, datetime

# Regex and Validators

class UserManager(models.Manager):

    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least two characters long!'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least two characters long!'
        if len(postData['email']) < 3:
            errors['email'] = 'Valid email address is required.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        else:
            userEmail = User.objects.filter(email = postData['email'])
            if len(userEmail) > 0:
                errors['unavailable'] = 'Email already exists. Please register with a different email or log in.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = 'Passwords do not match.'
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = 'Please enter an email address.'
        else:
            user = User.objects.filter(email = postData['email'])
            if len(user) == 0:
                errors['none'] = 'E-mail not registered.'
            else:
                logged_user = user[0]
                if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                    errors['password'] = 'Password is incorrect.'
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors={}
        if len(postData['title']) < 3:
            errors['title'] = 'Title should be at least three characters long!'
        if len(postData['description']) < 3:
            errors['description'] = 'Description should be at least three characters long!'    
        if len(postData['location']) < 3:
            errors['location'] = 'Location should be at least three characters long!'
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    user = models.ForeignKey(User, related_name="jobs", on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManager()