# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Imagen, ImageForm, UserForm


# Create your views here.

def index(request):
    if request.user.is_authenticated():
        lista_imagenes = Imagen.objects.filter(user=request.user)
    else:
        lista_imagenes = Imagen.objects.all()
    context = {'lista_imagenes': lista_imagenes}
    return render(request, 'polls/index.html', context)


def add_image(request):
    if request.method == 'POST':  # si el usuario esta enviando el fomrulario con datos
        form = ImageForm(request.POST, request.FILES)  # Bound form
        if form.is_valid():
           new_imagen = Imagen(url = request.POST['url'],
                               title = request.POST['title'],
                               description = request.POST['description'],
                               type = request.POST.get('type'),
                               imageFile = request.FILES['imageFile'],
                               user = request.user);
           new_imagen.save()

           return HttpResponseRedirect(reverse('images:index'))
    else:
        form = ImageForm()  # Unbound form

    return render(request, 'polls/image_form.html', {'form': form})

def add_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            return HttpResponseRedirect(reverse('images:index'))
    else:
       form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'polls/registro.html',context)

def login_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('images:index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('images:index'))
        else:
            mensaje = 'Nombre de usuario o clave no valido'

    return render(request, 'polls/login.html', {'mensaje': mensaje})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('images:index'))