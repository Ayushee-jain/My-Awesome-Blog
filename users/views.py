from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# decorators adds functionlity to an existing function in our case it will add functionality to our profile view where the user must be logged in to see profile page
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # is_valid() will check whether there is empty row or not if yes it will return false
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            # for alert that your form is successfully submitted
            messages.success(request,f'Your account has been created! You are now able to Login') 
            # if our registeration is successfull then we will go back to out blog's home page 
            return redirect('login')  
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

# options for messages
# messages.debug
# messages.info
# messages.warning
# messages.error
# messages.success

@login_required
def profile(request):
    if request.method == 'POST':  
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)