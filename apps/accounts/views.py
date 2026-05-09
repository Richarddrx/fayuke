from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import ProgrammingError

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Compte créé avec succès !')
                return redirect('dashboard:home')
            except ProgrammingError:
                messages.error(request, 'Erreur BD: appliquez d\'abord les migrations via /_migrate/.')
                return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
