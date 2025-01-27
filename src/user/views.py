from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from user.forms import SignUpForm, UserAuthentication

def signup_view(request):
    context={}
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            login(request, account)
            return redirect('welcome')
        else:
            context['signup_form'] = form
    else:
        form = SignUpForm()
        context['signup_form'] = form
    return render(request, 'user/signup.html', context)

def sign_out(request):
    logout(request)
    return redirect ('welcome')

def login_view(request):
    # Initialize an empty context dictionary #
    context = {}
    # Get the current user from the request object #
    user = request.user
    if user.is_authenticated:
        return redirect("welcome")

    if request.POST:
        # Bind the POST data to the UserAuthentication form #
        form = UserAuthentication(request.POST)
        if form.is_valid():
            # Extract the username and password from the POST data #
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate the user with the provided credentials #
            user = authenticate(username=username, password=password)

            # If authentication is successful, log the user in and redirect to the 'welcome' page #
            if user:
                login(request, user)
                return redirect("welcome")

    # If the request method is not POST or the form is invalid, render the login form #
    else:
            form = UserAuthentication() # Initialize an empty login form #

    # Add the form to the context dictionary #
    context['signin_form'] = form
    return render(request, 'user/login.html', context)