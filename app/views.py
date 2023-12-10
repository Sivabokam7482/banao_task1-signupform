from django.shortcuts import render,redirect
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.core.exceptions import ValidationError


from django.contrib.auth.decorators import login_required
# Create your views here.

def Dashboard(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        
        return render(request,'dashboard.html',d)
    return render(request,'dashboard.html')



def Doctor_signup(request):
    if request.method =='POST' and request.FILES:
        form=DoctorForm(request.POST,request.FILES)
        
        if form.is_valid():
            doctor=form.save(commit=False)
            password=doctor.cleaned_data['password']
            confirm_password=doctor.cleaned_data['confirm_password']
            if password and confirm_password and password == confirm_password:
                doctor.set_password(confirm_password)
                doctor.save()
            raise ValidationError("Password and confirm password do not match.")
     
        return HttpResponse('Registration Successfully')
    else:
        form=DoctorForm()

    return render(request,'doctor_signup.html',{'form':form})

def userlogin(request):
    if request.method =='POST':
        username=request.POST['un']
        password=request.POST['pw']
        doctor=authenticate(username=username,password=password)
        
        if doctor and doctor.is_active:
            login(request,doctor)
            request.session['username']=username

            return HttpResponseRedirect(reverse('Dashboard'))
        else:
            return HttpResponse('you are not an authenticated user')

    return render(request,'user_login.html')








def Patient_signup(request):
    if request.method =='POST' and request.FILES:
        form=PatientForm(request.POST,request.FILES)
        if form.is_valid():
            patient=form.save(commit=False)
            password=patient.cleaned_data['password']
            confirm_password=patient.cleaned_data['confirm_password']
            if password and confirm_password and password == confirm_password:
                patient.set_password(confirm_password)
                patient.save()
            raise ValidationError("Password and confirm password do not match.")

        return HttpResponse('Registration Successfully')

    else:
        form=PatientForm()

    return render(request,'patient_signup.html',{'form':form})
     
def userlogin(request):
    if request.method =='POST':
        username=request.POST['un']
        password=request.POST['pw']
        patient=authenticate(username=username,password=password)
        
        if patient and patient.is_active :
            login(request,patient)
            request.session['username']=username

            return HttpResponseRedirect(reverse('Dashboard'))
        else:
            return HttpResponse('you are not an authenticated user')

    return render(request,'user_login.html')









@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Dashboard'))

@login_required
def profiledisplay(request):
    fn=request.session.get('first_name')
    ln=request.session.get('last_name')
    em=request.session.get('email')
    ci=request.session.get('city')
    po=request.session.get('profile_picture')
    if  Patient:
        UO=Patient.objects.get(first_name=fn,last_name=ln,email=em,city=ci,profile_picture=po)
    else:
        DO=Doctor.objects.get(first_name=fn,last_name=ln,email=em,city=ci,profile_picture=po)

 
    d={'uo':UO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['password']
        un=request.session.get('username')
        if request.Patient.is_Patient:
            UO=PatientForm.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponse('patient password is changed successfully')

        else:
            DO=DoctorForm.objects.get(username=un)
            DO.set_password(pw)
            DO.save()
            return HttpResponse('Doctor password is changed successfully')

    return render(request,'changepassword.html')

def reset_password(request):
   
   if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        if request.Patient.is_Patient:
            LUO=Patient.objects.filter(username=un)
            
            if LUO:
                UO=LUO[0]
                UO.set_password(pw)
                UO.save()
                return HttpResponse('Patient password reset is Done')
            else:
                return HttpResponse('Patient user is not present in my DataBase')    
        else:
            DUO=Doctor.objects.filter(username=un)
            
            if DUO:
                UO=DUO[0]
                UO.set_password(pw)
                UO.save()
                return HttpResponse('Doctor password reset is Done')
            else:
                return HttpResponse('Doctor user is not present in my DataBase')    
            
   return render(request,'resetpassword.html')

