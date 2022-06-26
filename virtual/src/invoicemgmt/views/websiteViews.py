from typing import Counter
from django.contrib import auth
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import View
from random import randrange
from ..forms import *
from ..models import *
from ..filters import *
from datetime import datetime
import folium


# @login_required
def website_home(request):
    home_contents = Home_contents.objects.get()
    home_slides = Home_slides.objects.all()
    company_info = CompanyInfo.objects.get()
    partners = Partners.objects.all()
    context = {
        'title': 'Interstate Farm Ltd',
        'home_slides': home_slides,
        'home_contents': home_contents,
        'company_info': company_info,
        'partners': partners,

    }
    return render(request, 'website/home.html', context)

# @login_required


def services(request):
    company_info = CompanyInfo.objects.get()
    services = Services.objects.all()
    context = {
        'company_info': company_info,
        'services': services,
        'title': 'OURS SERVICES',
    }
    return render(request, 'website/services.html', context)

# @login_required


def news(request):
    company_info = CompanyInfo.objects.get()
    context = {
        'company_info': company_info,
        'title': 'NEWS',
    }
    return render(request, 'website/news.html', context)

# @login_required


def team(request):
    company_info = CompanyInfo.objects.get()
    teams = Teams.objects.all()
    context = {
        'company_info': company_info,
        'teams': teams,
        'title': 'OUR TEAM',
    }
    return render(request, 'website/team.html', context)

# @login_required


def careers(request):
    company_info = CompanyInfo.objects.get()
    careers = Careers.objects.filter(status=1)
    context = {
        'company_info': company_info,
        'careers': careers,
        'title2': ' JOB OPPORTUNITY',
        'title': 'CAREERS',
    }
    return render(request, 'website/careers.html', context)


def careersDetails(request, id):
    company_info = CompanyInfo.objects.get()
    careersDetails = get_object_or_404(Careers, pk=id)
    careersDuties = CareerDuties.objects.filter(career=id)
    careersExp = CareerExperience.objects.filter(career=id)
    context = {
        'company_info': company_info,
        'career': careersDetails,
        'careersDuties': careersDuties,
        'careersExp': careersExp,
        'title': 'Careers Details',
    }
    return render(request, 'website/careers_details.html', context)


def careersApply(request, id):
    company_info = CompanyInfo.objects.get()
    careerDetails = get_object_or_404(Careers, pk=id)
    if request.method == 'POST':
        form = CareerApply(request.POST, request.FILES)
        if form.is_valid():
            career_title = careerDetails
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            personal_info = form.cleaned_data['personal_info']
            education = form.cleaned_data['education']
            experience = form.cleaned_data['experience']
            resume = form.cleaned_data['resume']
            letter = form.cleaned_data['letter']

            JobApplications.objects.create(
                career_title=career_title,
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                personal_info=personal_info,
                education=education,
                experience=experience,
                applied_on = datetime.today().strftime('%Y-%m-%d'),
                resume=resume,
                letter=letter
            )
            messages.success(
                request, 'Thank you! Your application has been successfully submitted!')
            return redirect('/careersApply/'+str(id))

    else:
        form = CareerApply()
    context = {
        'company_info': company_info,
        'career': careersDetails,
        'form': form,
        'title': 'Careers Details',
    }
    return render(request, 'website/careers_apply.html', context)


def contact_us(request):
    company_info = CompanyInfo.objects.get()
    context = {
        'company_info': company_info,
        'title2': 'FEEL FREE TO CONTACT US',
        'title': 'CONTACT US',
    }
    return render(request, 'website/contact_us.html', context)


def about_us(request):
    company_info = CompanyInfo.objects.get()
    about = AboutUs.objects.get()
    context = {
        'company_info': company_info,
        'about': about,
        'title': 'ABOUT US',
    }
    return render(request, 'website/about_us.html', context)


def add_farmers(request):
    company_info = CompanyInfo.objects.get()
    m = folium.Map()
    m = m._repr_html_()
    if request.method == 'POST':
        form = MkulimaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Asante, Taarifa za mkulima zimehifadhiwa!')
            return redirect('/add_farmers')

    else:
        form = MkulimaForm()
    context = {
        'company_info': company_info,
        'form': form,
        'm': m,
        'title': 'FOMU YA USAJILI',
    }
    return render(request, 'website/wakulima.html', context)
