import os
# import wfdb
from . import forms
from . import models
# import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
# from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404

def home(request):
    # context = models.recipeName.Desc(id=x)
    return HttpResponse("Hello World")

def login_patient(request):
    if request.user.is_authenticated:
        return redirect("new_page")

    if request.method == "POST":
        user_001 = request.POST.get("username").lower()
        pass_001 = request.POST.get("password")
    
        try:
            user_001 = User.objects.get(username=user_001)
        except User.DoesNotExist:
            messages.error(request, "No username matches.")
            return redirect("login")

        user_001 = authenticate(request, username=user_001, password=pass_001)

        if user_001:
            login(request, user_001)
            return redirect("recipe")
        else:
            messages.error(request, "Incorrect Password")
            return redirect("login")

    cont = {"present":"login_page"}

    return render(request,"login.html", cont)

def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            inter =  form.save(commit=False)
            inter.username = form.cleaned_data["username"].lower()
            inter.save()
            login(request, inter)
            return redirect("login")
        else:
            messages.error(request, form.errors)

    cont = {"registeration":form,"message":form.errors}
    return render(request,"login.html",cont)

def logout_patient(request):
    logout(request)
    return redirect("new_page")

@login_required(login_url="login")
def new_page(request):
    return render(request,"home.html",)

def recipe_name(request):
    nam = models.RecipeName.objects.all()
    cont = {'recipes':nam, "user":request.user}
    return render(request,'inventory.html',cont)

def recipe_desc(request,pk):
    desc = models.RecipeName.objects.get(recipe_name=pk)
    cont = {"man":desc, "req":request}
    return render(request,"detailed_name.html",cont)

@login_required(login_url="login")
def post_recipes(request):
    jerry = forms.Post_Recipes()
    if (request.method == 'POST'):
        jerry = forms.Post_Recipes(request.POST)
        if(jerry.is_valid()):
            hert = jerry.save(commit=False)
            hert.author = request.user
            hert.save()
            return redirect("recipe")

    cont = {"man" : jerry}
    return render(request,"post_recipe.html",cont)

@login_required(login_url="login")
def update_recipes(request,pk):
    ferry = models.RecipeName.objects.get(recipe_name=pk)

    if request.user != ferry.author:
        return HttpResponse(f"You are not allowed to update {ferry.recipe_name:*^100}")

    if(request.method == 'POST'):
        forms1 = forms.Post_Recipes(request.POST, instance = ferry)
        if forms1.is_valid():
            forms1.save()
            return redirect("detail", pk = ferry.recipe_name)
    else:
        forms1 = forms.Post_Recipes(instance = ferry)
    dict = {'gest':forms1,}
    return render(request,"update_recipe.html",dict)

@login_required(login_url="login")
def delete_recipe(request,pk):
    jurry89 = get_object_or_404(models.RecipeName, id = pk)

    if request.user != jurry89.author:
        return HttpResponse(f"You are not allowed to delete {jurry89.recipe_name:*^100}")

    if request.method == 'POST':
        jurry89.delete()
        return redirect('recipe')
    dict = {"man":jurry89}
    return render(request,"delete_recipe.html",dict)


@login_required(login_url='login')
def updateORcreate_patient(request):
    
    # Fetching the patient details
    try:
        patient_detail = models.PatientDetail.objects.get(user=request.user)
        patient_form = forms.PatientForm(instance=patient_detail)
        form_type = 'update'
    except models.PatientDetail.DoesNotExist:
        patient_detail = None
        patient_form = forms.PatientForm()
        form_type = 'create'

    if request.method == 'POST':
        patient_form = forms.PatientForm(request.POST, instance=patient_detail)
        if patient_form.is_valid():
            internal_form = patient_form.save(commit=False)
            internal_form.user = request.user
            internal_form.save()
            return redirect('update_patient_properties')
    
    return render(request, "patients.html",{"patient_form":patient_form, "form_type":form_type})


@login_required(login_url='login')
def patient_prop(request):
    patient_detail = models.PatientDetail.objects.get(user=request.user)
    properties = models.PatientProperty.objects.filter(patient=patient_detail).order_by('-timestamp').first()
    # form_type = 1 if properties else None

    if request.method == 'POST':
        prop_form = forms.PatientPropertiesForm(request.POST)
        if 'create' in request.POST and prop_form.is_valid() and prop_form.has_changed():
            new_properties = prop_form.save(commit=False)
            new_properties.patient = patient_detail  # Associate the new record with the patient
            new_properties.save()
            return redirect('upload_audio_record', ids = new_properties.pp_id)
        elif 'same' in request.POST:
            return redirect('upload_audio_record', ids = properties.pp_id)
        else:
            return HttpResponse("Something wrong has happened!!!.")
    else:
        prop_form = forms.PatientPropertiesForm(instance=properties)

    return render(request, "properties.html", {"prop": prop_form})



@login_required(login_url="login")
def audio_in(request, ids):
    gerry_001 = get_object_or_404(models.PatientProperty,pp_id = ids)
    if request.method == 'POST':
        gerry_002 = forms.AudioUploadForm(request.POST, request.FILES)
        if gerry_002.is_valid():
            audio_data = gerry_002.save(commit=False)
            audio_data.pp = gerry_001
            audio_data.save()
            return redirect('patient_detail')
    else:
        gerry_002 = forms.AudioUploadForm()
    dict_01 = {"audio_form":gerry_002,"pat_01": gerry_001}
    return render(request, "audio_upload.html", dict_01)



@login_required(login_url="login")
def patient_detail(request):
    patient = get_object_or_404(models.PatientDetail, user=request.user)
    pp = models.PatientProperty.objects.filter(patient = patient)
    # Contains all the audio files submitted by the user.....
    audio_info:dict = {}
    for i in pp:
        individual = models.AudioData.objects.filter(pp=i)
        audio_info[i.pp_id] = individual
    
    # print(audio_info)
    return render(request, 'patient_details.html', {'patient_one': patient, "audio_info": audio_info})


def prediction(request,pp_ids,audio_id):
    audio_data = models.AudioData.objects.get(audio_id=audio_id)
    pp_data = models.PatientProperty.objects.get(pp_id=pp_ids)

    
    script_path = os.path.join(settings.BASE_DIR, 'main.py')
    
    os.system(f'python {script_path}')


    return HttpResponse(f'Hello world!!!!{pp_ids},{audio_id}')
