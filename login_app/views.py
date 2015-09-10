from django.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
import base64


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(
                username=request.POST['email'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
            )
            print "User created successfully"
            if user:
                email = user.email
                activation_key = unicode(base64.urlsafe_b64encode(email))
                send_mail(
                    'Set Password',
                    #'Please Click below to activate your account ' + "http://morning-garden-7880.herokuapp.com/activate/"+activation_key,

                    'Please Click below to activate your account ' + "http://127.0.0.1:8000/activate/"+activation_key,
                    'zlemma301@gmail.com',
                    [email]
                )
                return render_to_response('registration/success.html', '',)
        except Exception as e:
            print e

    return render_to_response(
        'registration/register.html'
        '',
    )


@csrf_exempt
def activate_user(request, activation_key):
    if request.method == "GET":
        return render_to_response(
            'registration/set_password.html'
            '',
        )
    dec_email = base64.urlsafe_b64decode(activation_key.encode('utf-8'))
    u = User.objects.get(email=dec_email.strip())
    new_password = request.POST['new_password']
    u.set_password(new_password)
    u.is_active = True
    u.save()
    return render_to_response(
        'registration/password_success.html'
        '',
    )



@csrf_exempt
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        request.session.set_expiry(30)
        auth.login(request, user) # Correct password, and the user is marked "active"
        # Redirect to a success page.
        return render_to_response(
            'home.html',
            '',
        )
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")



def logout_page(request):
    request.session.set_expiry(30)
    logout(request)
    return HttpResponseRedirect('/') # Redirect to a success page.


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )

@login_required
def home(request):
    request.session.set_expiry(30)
    return render_to_response(
        'home.html',
        {'user': request.user}
    )


