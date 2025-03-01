from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import re
from django.contrib import messages
from django.contrib import auth
import openai
from .models import usermessages, dietplan
from django.utils.safestring import mark_safe

#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

openai.api_key = "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"

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def bmi(request):
    weight=float(request.GET.get('weight',0))
    height=float(request.GET.get('height',0))
    try:
        bmi=round(weight/(height**2),2)
    except:
        bmi=0
    context={'bmi':bmi}

    return render(request, "bmi.html",context)

def calculator(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        cnf_password=request.POST['cnf_password']

        if password==cnf_password:
            if User.objects.filter(username=username):
                messages.success(request, f"Email Already Exist! Please Try Again.")
                print("user alredy exist")
                return redirect('/signup')
            elif User.objects.filter(email=email):
                messages.success(request, f"Email Already Exist! Please Try Again.")
                print("email alredy exist")
                return redirect('/signup')
            else:
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
                pat = re.compile(reg)            
                mat = re.search(pat, password)
                if mat:
                    User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    print("Student User Register successful")
                    return redirect('/')
                else:
                    messages.success(request, f"Password should contain one uppercase, one lowercase, one number and one special symbol")
                    print("Password invalid !!")
                    return redirect('/signup') 

    return render(request, 'signup.html')

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print('user login successfully')
            return redirect('/')
        else:
            messages.success(request, f"Wrong Credientials! Please Try Again..") 
            return redirect('/signin') 

    else:
        return render(request,'signin.html')
        
    
@login_required(login_url='')
def logout_user(request):
    auth.logout(request)
    return redirect('/')

# def chat_app(request):
#     if request.method=="POST":
#         openai.api_key = "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"
#         chat=request.POST['chat']
#         conversation = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=chat,
#         temperature=0.7,
#         max_tokens=1024,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         )
        
#         print(conversation.choices[0].text)
#         usermessages.objects.create(user=request.user,messagefromuser=chat,messagefromCHatGpt=conversation.choices[0].text)
#         return redirect('/chat_app')
#     msg=usermessages.objects.filter(user=request.user)
#     return render(request,'chat_app.html',{"msg":msg})

def chat_app(request):
    if request.method == "POST":
        chat = request.POST.get("chat", "").strip()
        if not chat:
            return redirect('chat_app')  # Prevent empty submissions

        try:
            conversation = openai.Completion.create(
                engine="text-davinci-002",
                prompt=chat,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            response_text = conversation.choices[0].text.strip()

            # Save message to database
            usermessages.objects.create(
                user=request.user,
                messagefromuser=chat,
                messagefromCHatGpt=response_text
            )
        except Exception as e:
            print(f"Error: {e}")

        return redirect('chat_app')

    msg = usermessages.objects.filter(user=request.user)
    return render(request, 'chat_app.html', {"msg": msg})

def dietplanview(request):
    if request.method=="POST":
        age=request.POST['age']
        gender=request.POST['gender']
        calorygoal=request.POST['calorygoal']
        cuisine=request.POST['cuisine']

        chat=f"Write a Dite Plan for {age} of {gender} to get {calorygoal} calories in {cuisine} cuisine for a week."
        openai.api_key = "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"
        conversation = openai.Completion.create(
        engine="text-davinci-002",
        prompt=chat,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )
        
        text=conversation.choices[0].text

        richtext = mark_safe("<p>" + text.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>")

        dietplan.objects.create(user=request.user,dietplan=richtext)
        return redirect('/dietplan')
    
    ans=None
    if dietplan.objects.filter(user=request.user).exists():
        ans= dietplan.objects.filter(user=request.user).last()
        print(ans)
    
    context={'dietplan':ans}

    return render(request,'dietplan.html',context)