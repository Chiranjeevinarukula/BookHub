from django.shortcuts import render,redirect,reverse
from .forms import signUpForm,ProfileForm,UserForm
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


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

class CurrentUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not request.user.id != user_id:
            return HttpResponseForbidden("You do not have permission to edit this user.")
        return super().dispatch(request, *args, **kwargs)
    
class ProfileUpdateView(CurrentUserRequiredMixin,View):
    def get(self,request):
        form=UserForm()
        profileUpdateForm = ProfileForm()
        return render(request,'account/profileUpdate.html',{'form': form,'profileform':profileUpdateForm})
    
    def post(self,request):
        user=request.user
        form = UserForm(request.POST,instance=user)
        profileUpdateForm = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid() and profileUpdateForm.is_valid():
            form.save()
            profileUpdateForm.save()
            return redirect(reverse('profile',args=[user.pk]))
        return render(request,'account/profileUpdate.html',{'form': form,'profileform':profileUpdateForm})

