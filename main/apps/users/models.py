# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']:
                errors['duplicate_email'] = "Email already in database"
        if len(postData['email']) < 1:
            errors["empty_email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid Email Address!"
        if len(postData['first_name']) < 1:
            errors["empty_first_name"] = "First name cannot be empty!"
        if any(i.isdigit() for i in postData['first_name']) == True:
            errors["invalid_first_name"] = "Invalid first name!"
        if len(postData['last_name']) < 1:
            errors["empty_last_name"] = "Last name cannot be empty!"
        if any(i.isdigit() for i in postData['last_name']) == True:
            errors["invalid_last_name"] = "Invalid last name!"
        if len(postData['password']) < 8:
            errors["short_password"] = "Password must contain at least eight characters!"
        if postData['confirm_password'] != postData['password']:
            errors["password_does_not_match"] = "Passwords must match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData['email']):
            errors['unregistered'] = "Invalid Email!"
        else:
            user = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == True:
                pass
            else:
                errors['invalid_password'] = "Invalid Password!"
        return errors
    def update_info_validator(self, postData, user_id):
        errors = {}
        users = User.objects.all()
        for user in users:
            if user.email == postData['email']:
                if not user.id != User.objects.filter(id = user_id):
                    errors['duplicate_email'] = "Email already in database"
        if len(postData['email']) < 1:
            errors["empty_email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = "Invalid Email Address!"
        if len(postData['first_name']) < 1:
            errors["empty_first_name"] = "First name cannot be empty!"
        if any(i.isdigit() for i in postData['first_name']) == True:
            errors["invalid_first_name"] = "Invalid first name!"
        if len(postData['last_name']) < 1:
            errors["empty_last_name"] = "Last name cannot be empty!"
        if any(i.isdigit() for i in postData['last_name']) == True:
            errors["invalid_last_name"] = "Invalid last name!"
        return errors
    def update_password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["short_password"] = "Password must contain at least eight characters!"
        if postData['confirm_password'] != postData['password']:
            errors["password_does_not_match"] = "Passwords must match!"
        return errors
    def description_validator(self, postData):
        errors = {}
        if len(postData['description']) < 1:
            errors["empty_description"] = "Description cannot be empty!"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField(default=1)
    description = models.CharField(default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['message_input']) < 1:
            errors["empty_message"] = "Message cannot be blank!"
        return errors
class Message(models.Model):
    messagee = models.ForeignKey(User, related_name='messagee')
    messager = models.ForeignKey(User, related_name='messager')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['comment_input']) < 1:
            errors["empty_comment"] = "Comment cannot be blank!"
        return errors
class Comment(models.Model):
    message = models.ForeignKey(Message)
    commenter = models.ForeignKey(User)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()