from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from flask_login import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.contrib import messages

from mainpage.forms import ProfileForm, SignUpForm, UserForm

from .models import  Todo, Profile


def homeview(request):
    to = Todo()
    if request.method == 'POST':
        taskinput = request.POST['taskinput']
        to.task = taskinput
        to.user_id = request.user.id
        to.save()
        return HttpResponseRedirect("/")
    return render(request, 'home.html', {'tasks': Todo.objects.all()})


def deletetask(request, task_id=None):
    to = Profile.objects.get(id=task_id)
    to.delete()
    return HttpResponseRedirect("/")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
