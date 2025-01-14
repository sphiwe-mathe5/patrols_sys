from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, PasswordResetRequest
from django.utils.crypto import get_random_string


def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                
                password=password,
            )

            login(request, user, backend='submit.backends.EmailBackend')

            messages.success(request, 'Signup successful!')
            return redirect('index')
        
        except IntegrityError:
            messages.error(request, 'An account with this email already exists. Please log in or use a different email.')

            return redirect('signup')  

    return render(request, 'submit/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Attempting to log in with email: {email}")  

        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("Authentication successful")  
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            print("Authentication failed")  
            messages.error(request, 'Invalid credentials')
    return render(request, 'submit/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found.')

    return render(request, 'submit/login.html')


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'submit/reset_password.html', {'token': token})



def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'submit/reset_password.html', {'token': token})
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'submit/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {'u_form': u_form,}

    return render(request, 'submit/profile.html', context)

    


