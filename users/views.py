from django.shortcuts import render from django.views import View from django.contrib import messages from django.http import HttpResponseRedirect from django.contrib.auth import authenticate, login, logout from orders import models as order_models from . import models as user_models

class Login(View): def get(self, request): if request.user.is_authenticated: return HttpResponseRedirect("/") if request.GET.get("next"): request.session["next"] = request.GET.get("next") return render(request, "user/login.html")

def post(self, request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/")

    messages.error(request, "Invalid email or password", "alert-danger")
    if request.session.get("next"):
        return HttpResponseRedirect(request.session.get("next"))
    return HttpResponseRedirect(request.path_info)

class Register(View): def get(self, request): if request.user.is_authenticated: return HttpResponseRedirect("/") if request.GET.get("next"): request.session["next"] = request.GET.get("next") return render(request, "user/signup.html")

def post(self, request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    first_name = request.POST.get("first-name")
    last_name = request.POST.get("last-name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password2 = request.POST.get("confirm-password")

    if password != password2:
        messages.error(request, "Passwords do not match", "alert-danger")
        return HttpResponseRedirect(request.path_info)

    if user_models.User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists", "alert-danger")
        return HttpResponseRedirect(request.path_info)

    user = user_models.User.objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    user.save()

    messages.success(request, "Account created successfully", "alert-success")
    login(request, user)
    if request.session.get("next"):
        return HttpResponseRedirect(request.session.get("next"))
    return HttpResponseRedirect("/")

def logout_view(request): logout(request) return HttpResponseRedirect("/")

class Profile(View): def get(self, request): if not request.user.is_authenticated: return HttpResponseRedirect("/login?next=/profile/")

orders = order_models.Orders.objects.filter(user=request.user)
    address = user_models.Addresses.objects.filter(user=request.user)
    return render(
        request,
        "user/profile.html",
        {
            "user": request.user,
            "orders": orders,
            "addresses": address,
        },
    )

def post(self, request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login?next=/profile/")

    form = request.POST.get("form")
    if form == "profileInfo":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_models.User.objects.filter(id=request.user.id).update(
            first_name=first_name, last_name=last_name
        )
        messages.success(request, "Profile updated successfully", "alert-success")
    elif form == "changePassword":
        currentPassword = request.POST.get("currentPassword")
        newPassword = request.POST.get("newPassword")
        confirmPassword = request.POST.get("confirmPassword")

        if newPassword != confirmPassword:
            messages.error(request, "Passwords do not match", "alert-danger")
            return HttpResponseRedirect(request.path_info)

        if newPassword == currentPassword:
            messages.error(request, "New password cannot be same as current password", "alert-danger")
            return HttpResponseRedirect(request.path_info)

        if not request.user.check_password(currentPassword):
            messages.error(request, "Current password is incorrect", "alert-danger")
            return HttpResponseRedirect(request.path_info)

        request.user.set_password(newPassword)
        request.user.save()
        messages.success(request, "Password changed successfully", "alert-success")

    return HttpResponseRedirect("/profile/")

