from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

# Create your views here.


def login(request):
    if request.method == 'POST': #Signup button was clicked
        global mail 
        mail = request.POST.get ('email')
        passw = request.POST.get ('password')

        user = auth.authenticate(username=mail, password=passw)

        if user is not None:
            auth.login(request, user)
            context = {'user' : mail}
            #return render(request, "welcome.html", context)
            return redirect(welcome)
        else:
            context = {'error' : "Authentication Failed!"}
            return render(request, "login.html", context)
    else:
        #This is a GET Operation, so just return the page as it is.
        return render(request, "login.html")


def signup(request):
    mail_error = ""
    pass_error = ""
    response = ""
    if request.method == "POST": #Signup button was clicked
        #data = User()
        #post_data = request.POST
        mail = request.POST.get ('email')
        if User.objects.filter(email__iexact=mail).exists(): #Check if email already exists in the database
            mail_error = "Email already exists!"

            context = {'mail_error': mail_error}
            return render(request, 'signup.html', context)
        elif mail == "":
            mail_error = "Email cannot be null!"

            context = {'mail_error': mail_error}
            return render(request, 'signup.html', context)
    
        passw = request.POST.get ('password')
        retpassword = request.POST.get('retpassword') #The retyped password is not saved in the Database
        if retpassword != passw:
            pass_error = "Passwords do not match!"

            context = {'pass_error' : pass_error}
            return render(request, 'signup.html', context)
        elif passw == "":
            pass_error = "Password cannot be null!"

            context = {'pass_error' : pass_error}
            return render(request, 'signup.html', context)
            
        user = User.objects.create_user(username=mail, email=mail, password=passw)
        user.save()

                #data.username = post_data.get ('email') #Use email as username since this is supposed to be unique
                #data.email = post_data.get ('email')
                #data.password = post_data.get ('password')
                #data.save()
        response = "Registration Successfull!"

        context = {'message': response, 'mail_error': mail_error, 'pass_error' : pass_error}
        return render(request, 'signup.html', context)
    else:
        #This is a GET Operation, so just return the page as it is.
        return render(request, "signup.html")


def welcome(request):
    if request.method == "POST": #Logout button was clicked
        auth.logout(request)
        return redirect(login)
    else:
        context = {'user' : mail}
        return render(request, "welcome.html", context)