from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+')

def index(request):
    if not 'active_user' in request.session:
        request.session['active_user'] = ""
    return render(request, 'belt_app/index.html')

def success(request):
    if request.session['active_user'] == "" or not 'active_user' in request.session:
        messages.add_message(request, messages.ERROR, "Please Login to Continue")
        return redirect('/')
    else:
        loggedInUserID = request.session['active_user']['id']

        friends = models.Friend_list.objects.filter(user_id=loggedInUserID)

        get_more = models.Friend_list.objects.values_list('user', flat=True)
        get_more_more = models.User.objects.exclude(id=get_more)
        not_want = models.Friend_list.objects.exclude(id=get_more_more)

        friends_list = models.Friend_list.objects.filter(user_id=loggedInUserID)

        filtered_friends_list = []
        for friend in friends_list:
            filtered_friends_list.append(friend.friend)

        users = models.User.objects.exclude(friendsid=loggedInUserID)

        if len(friends) == 0:
            request.session['warning'] = True
        else:
            request.session['warning'] = False
        context = {
            "users" : users,
            "friends" : friends,
            "filtered_friends_list" : filtered_friends_list,
            "loggedInUserID" : loggedInUserID,
        }
        return render(request, 'belt_app/success.html', context)

def add_user(request):
    result = models.User.objects.register(request.POST)
    if result[0] == False:
        print result[1]
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        print result[1]
        return log_user_in(request, result[1])
    return redirect('/success')

def login(request):
    result = models.User.objects.login(request.POST)
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['active_user'] = {
        'id' : user.id,
        'name' : user.name,
        'alias' : user.alias,
        'email' : user.email,
    }
    return redirect ('/success')

def logout(request):
    del request.session['active_user']
    return redirect('/')

def user(request, id):
    user = models.User.objects.all()
    user_id = int(id)
    instance = models.User.objects.filter(id=user_id)
    print instance[0].birthday, "ppp"*100
    context = {
        "user": instance[0],

    }
    return render(request, 'belt_app/user.html', context)

def add_friend(request, id):
    user = models.User.objects.all()
    user_id = int(id)
    sessionID = request.session['active_user']['id']
    new_friend = models.Friend_list.objects.add_to_friends(user_id, sessionID)
    return redirect('/success')

def delete(request, id):
    friendship = models.Friend_list.objects.get(id=id)
    friendship_id = friendship.id
    delete = models.Friend_list.objects.delete_friend(friendship_id)
    return redirect('/success')

def delete_user(request, id):
    user = models.User.objects.get(id=id).delete()
    return redirect('/success')
