#authentication
from django.contrib.auth import (
	authenticate,
	login,
	logout,
	get_user_model,


	)
#http
from django.http import HttpResponse
from django.shortcuts import render,redirect
#forms
from .forms import UserLoginForm,UserRegisterForm

# Create your views here.


def login_view(request):
	n=request.GET.get('next')
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user=authenticate(username=username,password=password)
		login(request,user)
		if n:
			return redirect(n)
		return redirect("posts:home")
		

	context={
	"form":form,
	"title":"Login"
	}	

	return render(request,"form.html",context)

def register_view(request):
	n=request.GET.get('next')
	form=UserRegisterForm(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		password=form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user=authenticate(username=user.username,password=password)
		login(request,new_user)
		if n:
			return redirect(n)
		return redirect("posts:home")

	context={
	"title":"Register",
	"form":form,
	}

	return render(request,"form.html",context)

def logout_view(request):
	logout(request)

	return redirect("posts:home")		