# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm


class Imagen(models.Model):
    url = models.CharField(max_length=10000)
    title=models.CharField(max_length=150,blank=True)
    description=models.CharField(max_length=1000,null=True)
    type=models.CharField(max_length=5,blank=True)
    imageFile=models.ImageField(upload_to='images',null=True)
    user=models.ForeignKey(User,null=True)

class ImageForm(ModelForm):

    class Meta:
        model = Imagen
        fields = ['url','title','description','type','imageFile']

class UserForm(ModelForm):

    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2']

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registrado.')
        return email

    def clean_password2(self):
        """Comprueba que password y possword2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las claves no coinciden.')
        return password2

