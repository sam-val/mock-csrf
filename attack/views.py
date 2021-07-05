from os import name
from django.contrib.auth.decorators import login_required
import subprocess
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import WithdrewForm, Account
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User


@method_decorator(csrf_exempt, name='dispatch')
class MyLogin(auth_views.LoginView):
    template_name = "login.html"


@login_required
@csrf_exempt
def account(r):
    balance = r.user.account.balance
    form = WithdrewForm(initial={'current_balance' : balance, 'withdrew':0}) 
    return render(r, "balance.html", {'form': form})

def regenerate_table(r):
    balance = 5000
    name = 'name'
    passw = '123'
    # run in the command-line:
    subprocess.run(['./manage.py', 'reset_db', '--noinput', '--close-sessions']) # reset db using the django_extensions module; it destroys the whole db
    subprocess.run(['./manage.py','migrate']) # apply all migrations 

    queries = f"u = User.objects.create_user(username='{name}', password='{passw}')"
    queries += f"\nAccount.objects.create(user=u, balance={balance})"
    # queries += "\n"
    
    subprocess.run(['./manage.py','shell_plus', '--quiet-load','-c', queries])
    
    return HttpResponseRedirect(reverse('login'))

import sys

@login_required
@csrf_exempt
def withdrew(r):
    if r.method == 'POST':
        if r.user.is_authenticated:
            hack = ''
            try:
                hack = r.POST['hack']
            except KeyError:
                print("key error" , file=sys.stderr)

            account = Account.objects.filter(user=r.user).first()
            form = WithdrewForm({'withdrew': r.POST['withdrew'], 'current_balance': account.balance})
            if form.is_valid():
                withdrew_amount = form.cleaned_data['withdrew']
                account.balance -= withdrew_amount
                account.save()
                return HttpResponseRedirect(reverse('account') + f"?hack={hack}")
            else:
                return render(r, "balance.html", {'form': form})
        else:
            print("not authenticated", file=sys.stderr)
                
    return HttpResponseBadRequest()
    

 