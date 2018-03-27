# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(req):
    return render(req, 'users/index.html')
def signin(req):
    return render(req, 'users/signin.html')
def register(req):
    return render(req, 'users/register.html')

def create(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/register')
    if len(User.objects.all()) < 1:
        User.objects.create(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()), user_level = 9)
    else:
        User.objects.create(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()))
    req.session['active_name'] = User.objects.last().first_name
    req.session['active_id'] = User.objects.last().id
    req.session['logged_user_level'] = User.objects.last().user_level
    if req.session['logged_user_level'] == 9:
        return redirect('/dashboard/admin')
    elif req.session['logged_user_level'] == 1:
        return redirect('/dashboard')

def login(req):
    errors = User.objects.login_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/signin')
    loggedUser = User.objects.get(email = req.POST['email'])
    req.session['active_name'] = loggedUser.first_name + loggedUser.last_name
    req.session['active_id'] = loggedUser.id
    req.session['logged_user_level'] = loggedUser.user_level
    if req.session['logged_user_level'] == 9:
        return redirect('/dashboard/admin')
    elif req.session['logged_user_level'] == 1:
        return redirect('/dashboard')

def logoff(req):
    req.session.clear()
    return redirect('/')

def dashboard(req):
    context = {
        'users': User.objects.all(),
        'logged_user_level': req.session['logged_user_level']
    }
    return render(req, 'users/dashboard.html', context)

def show(req, user_id):
    context = {
        'user': User.objects.get(id = user_id),
        'wall_messages': Message.objects.filter(messagee = user_id).order_by('-created_at'),
        'comments': Comment.objects.all(),
        'logged_user_level': req.session['logged_user_level']
    }
    return render(req, 'users/show.html', context)

def message(req, user_id):
    errors = Message.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/users/show/{}'.format(user_id))
    Message.objects.create(messagee = User.objects.get(id = user_id), messager = User.objects.get(id = req.session['active_id']), message = req.POST['message_input'])
    return redirect('/users/show/{}'.format(user_id))

def comment(req, user_id, message_id):
    errors = Comment.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/users/show/{}'.format(user_id))
    Comment.objects.create(message = Message.objects.get(id = message_id), commenter = User.objects.get(id = req.session['active_id']), comment = req.POST['comment_input'])
    return redirect('/users/show/{}'.format(user_id))

def edit(req):
    context = {
        'user': User.objects.get(id = req.session['active_id']),
        'logged_user_level': req.session['logged_user_level']
    }
    return render(req, 'users/edit.html', context)

def update_info(req, user_id):
    errors = User.objects.update_info_validator(req.POST, user_id)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        if req.session['logged_user_level'] == 9:
            return redirect('/users/edit/{}'.format(user_id))
        elif req.session['logged_user_level'] == 1:
            return redirect('/users/edit')
    User.objects.filter(id = user_id).update(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'])
    return redirect('/users/show/{}'.format(user_id))

def update_password(req, user_id):
    errors = User.objects.update_password_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        if req.session['logged_user_level'] == 9:
            return redirect('/users/edit/{}'.format(user_id))
        elif req.session['logged_user_level'] == 1:
            return redirect('/users/edit')
    User.objects.filter(id = user_id).update(password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()))
    return redirect('/users/show/{}'.format(user_id))

def description(req, user_id):
    errors = User.objects.description_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        if req.session['logged_user_level'] == 9:
            return redirect('/users/edit/{}'.format(user_id))
        elif req.session['logged_user_level'] == 1:
            return redirect('/users/edit')
    User.objects.filter(id = user_id).update(description=req.POST['description'])
    return redirect('/users/show/{}'.format(user_id))

def admin_dashboard(req):
    context = {
        'users': User.objects.all(),
        'logged_user_level': req.session['logged_user_level']
    }
    return render(req, 'users/admin_dashboard.html', context)

def admin_edit(req, user_id):
    context = {
        'user': User.objects.get(id = user_id),
        'logged_user_level': req.session['logged_user_level']
    }
    return render(req, 'users/edit.html', context)

def delete(req, user_id):
    temp = User.objects.get(id = user_id)
    temp.delete()
    return redirect('/dashboard/admin')

def add(req):
    return render(req, 'users/new.html')

def new(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/register')
    User.objects.create(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()))
    return redirect('/dashboard/admin')