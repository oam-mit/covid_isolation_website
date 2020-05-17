from django.shortcuts import render,reverse
from django.contrib.auth import logout
from django.contrib import messages as mess
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm

# Create your views here.
def check_staff(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('feeds:index'))
    else:
        logout(request)
        mess.error(request,'Only Staff members are allowed',extra_tags='danger')
        return HttpResponseRedirect(reverse('users:login'))

def register(request):
    context={}
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            mess.success(request,'Your request for registration is recorded. If approved, you will be able to login')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            mess.error(request,'Check form details',extra_tags='danger')
            context['form']=form
            return render(request,template_name='users/register.html',context=context)
    else:
        context['form']=CustomUserCreationForm()
        return render(request,template_name='users/register.html',context=context)
