from django.shortcuts import render,redirect
from .forms import signUpForm
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User


# Create your views here.

class SignUpView(View):
    def get(self, request):
        form = signUpForm()
        return render(request, 'account/signup.html', {'form': form})
    def post(self, request):
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('get_books')  # Redirect to the desired URL upon successful signup
        return render(request, 'account/signup.html', { 'form': form })

def profileView(request,pk):
    user=User.objects.get(id=pk)
    return render(request,'account/profile.html',{'user':user})