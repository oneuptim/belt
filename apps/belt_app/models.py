from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+')

# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        login_email = post['login_email']
        login_password = post['login_password']

        errors =[]

        user_list = User.objects.filter(email = login_email)

        if len(login_email) < 1:
            errors.append('Email is required')
        if len(login_password) < 1:
            errors.append('Password is required')
        if user_list:
            active_user = user_list[0]
            password = login_password.encode()
            if bcrypt.hashpw(password, active_user.pw_hash.encode()) == user_list[0].pw_hash :
                return (True, active_user)
            else:
                errors.append('Email and password do not match')
        else:
            errors.append('Email does not exist')
        return (False, errors)

    def register(self, post):
        name = post['name']
        alias = post['alias']
        email = post['email']
        password = post['password']
        confirm_password = post['confirm_password']
        birthday = post['birthday']

        birthday_month = birthday[5:7]
        birthday_day = birthday[8:10]
        birthday_year = birthday[0:4]

        errors = []
        user_list = User.objects.filter(email = email)
        if len(name) < 1:
            errors.append('Name is required')
        if len(alias) < 1:
            errors.append('Alias is required')
        if not name_regex.match(name):
            errors.append('Name must only contain letters')
        if not name_regex.match(alias):
            errors.append('Alias must only contain letters')
        if not EMAIL_REGEX.match(email):
            errors.append('Email is invalid!')
        if user_list:
            errors.append('Email already exists!')
        if len(password) < 1:
            errors.append('Password is required')
        if len(password) < 8:
            errors.append('Password must have more than 8 characters')
        if password != confirm_password:
            errors.append('Passwords do not match!')
        if len(birthday) < 0:
            errors.append('Please Enter Birthday')
        if len(birthday) < 10:
            errors.append('Please Enter Valid Birthday')
        if len(birthday) > 9:
            if int(birthday_year) > 2016:
                errors.append('Please Enter Valid Brithday Year')
        if len(errors) > 0:
            return (False, errors)
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = self.create(name=name, alias=alias, email=email, pw_hash=pw_hash, birthday=birthday)
        return (True, user)

    def delete_user(self, userid):
        deleteUser = self.get(id=id).delete()
        return

class Friend_listManager(models.Manager):
    def add_to_friends(self, friend_id, sessionID):
        user = User.objects.get(id=sessionID)
        friend = User.objects.get(id=friend_id)

        test = self.all()

        add_new_friend = self.create(user=user, friend=friend)
        return "hello"

    def delete_friend(self, id):
        delete_it = self.get(id=id).delete()
        return "hello"




class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    birthday = models.CharField(max_length=45, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friend_list(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name="usersid")
    friend = models.ForeignKey('User', models.DO_NOTHING, related_name ="friendsid")
    objects = Friend_listManager()
