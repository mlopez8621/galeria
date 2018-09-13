# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Imagen, ImageForm, UserForm


# Create your views here.
@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        lista_imagenes = Imagen.objects.filter(user=request.user)
    else:
        lista_imagenes = Imagen.objects.all()
    context = {'lista_imagenes': lista_imagenes}
    return HttpResponse(serializers.serialize("json", lista_imagenes))

@csrf_exempt
def add_image(request):
    if request.method == 'POST':  # si el usuario esta enviando el fomrulario con datos
           new_imagen = Imagen(url = request.POST['url'],
                               title = request.POST['title'],
                               description = request.POST.get('description'),
                               type = request.POST.get('type'),
                               imageFile = request.FILES['imageFile'],
                               user = request.user);
           new_imagen.save()
    return HttpResponse(serializers.serialize("json",[new_imagen]))

@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        jsonUser=json.loads(request.body)
        username = jsonUser['username']
        first_name = jsonUser['first_name']
        last_name = jsonUser['last_name']
        password = jsonUser['password']
        email = jsonUser['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return HttpResponse(serializers.serialize("json", [user_model]))

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        JsonUser=json.loads(request.body)
        username = JsonUser['username']
        password = JsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            mensaje = "ok"
        else:
            mensaje = 'Nombre de usuario o clave no valido'

    return JsonResponse({"mensaje":mensaje})

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"mensaje":'ok'})

@csrf_exempt
def islogged_view(request):
    if request.user.is_authenticated():
        mensaje = 'ok'
    else:
        mensaje = 'no'

    return JsonResponse({"mensaje":mensaje})