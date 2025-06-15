from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .forms import CustomPasswordResetForm

def login_user(request):
    mes = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            request.session["login_error"] = "Invalid username or password"
            return redirect("login_user")
    mes = request.session.pop("login_error", "")
    return render(request, "registration/login.html", {"mes": mes})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")

        if password != password2:
            request.session["mes"] = "Passwords do not match."
            request.session["mes_type"] = False
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            request.session["mes"] = "Username already taken."
            request.session["mes_type"] = False
            return redirect("signup")

        if re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password) is None:
            request.session["mes"] = "Password must have at least one letter, one digit, and minimum 8 characters total."
            request.session["mes_type"] = False
            return redirect("signup")

        try:
            validate_email(email)
        except ValidationError:
            request.session["mes"] = "Please enter a valid email address."
            request.session["mes_type"] = False
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        request.session["mes"] = "Account created successfully!"
        request.session["mes_type"] = True
        return redirect("signup")

    mes = request.session.pop("mes", "")
    mes_type = request.session.pop("mes_type", False)

    return render(request, "registration/signup.html", {"mes": mes, "mes_type": mes_type})


def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password-reset-email.txt',
                subject_template_name='registration/password-reset-subject.txt',
            )
            return redirect("password-reset-done")
    else:
        form = CustomPasswordResetForm()

    return render(request, "registration/password-reset.html", {"form": form})
