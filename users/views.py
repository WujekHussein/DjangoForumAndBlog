from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .forms import UserRegistrationForm, UserLoginForm

from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Confirmation successful")
        return redirect('/')
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect('/')

def activateEmail(request, user, email):
    mail_subject = 'Activate your account'
    message = render_to_string('users/template_activate_account.html',
                               {'user': user,
                                'domain': get_current_site(request).domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                                'protocol': 'http'
                                })
    email = EmailMessage(mail_subject, message, to=[email])
    email.send()

    messages.success(request, f'A message with activation link has been sent to {email}')

def registration_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect("/")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {"form" : form})
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user(), )
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect("/")

    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form" : form})
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")