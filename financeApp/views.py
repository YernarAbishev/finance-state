from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCompanyForm, AddBalanceSheetForm, NewUserForm
from .models import Company, BalanceSheet
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def homePage(request):
    return render(request, "frontend/home.html")


def companyList(request):
    companies = Company.objects.all()
    return render(request, "frontend/company-list.html", {
        'companies': companies
    })

def addCompanyPage(request):
    if request.method == "POST":
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.info(request, f"Компания добавлена!")
            return redirect('homePage')
    else:
        form = AddCompanyForm()
    return render(request, "frontend/add-company.html", {
        'form': form
    })

def addBalanceSheet(request):
    if request.method == "POST":
        form = AddBalanceSheetForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.info(request, f"Отчет добавлен!")
            return redirect('homePage')
    else:
        form = AddBalanceSheetForm()

    return render(request, "frontend/add-document.html", {
        'form': form
    })



def documentPage(request):
    return render(request, "frontend/documents.html")


def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Здравствуйте, {username}.")
                return redirect("homePage")
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = AuthenticationForm()
    return render(request, "frontend/login.html", {
        'form': form
    })

def logoutUser(request):
    logout(request)
    messages.info(request, "Вы вышли из системы")
    return redirect("homePage")


def viewAssets(request, slug):
    company = None
    assets = BalanceSheet.objects.all()
    if slug:
        company = get_object_or_404(Company, slug=slug)
        assets = assets.filter(company=company)
    return render(request, "frontend/actives.html", {
        'assets': assets,
        'company': company
    })

def viewEquity(request, slug):
    company = None
    equaties = BalanceSheet.objects.all()
    if slug:
        company = get_object_or_404(Company, slug=slug)
        equaties = equaties.filter(company=company)
    return render(request, "frontend/equities.html", {
        'equaties': equaties,
        'company': company
    })

def viewRatios(request, slug):
    company = None
    ratios = BalanceSheet.objects.all()
    if slug:
        company = get_object_or_404(Company, slug=slug)
        ratios = ratios.filter(company=company)
    return render(request, "frontend/ratios.html", {
        'ratios': ratios,
        'company': company
    })

