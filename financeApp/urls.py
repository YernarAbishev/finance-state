from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('menu/documents/', views.documentPage, name='documentPage'),
    path('company/list/', views.companyList, name='companyList'),
    path('user/login/', views.loginPage, name='loginPage'),
    path('user/logout/', views.logoutUser, name='logoutUser'),
    path('view/assets/<slug:slug>/', views.viewAssets, name='viewAssets'),
    path('view/equity/<slug:slug>/', views.viewEquity, name='viewEquity'),
    path('view/ratios/<slug:slug>/', views.viewRatios, name='viewRatios'),
    path('add/balance-sheet/', views.addBalanceSheet, name='addBalanceSheet'),
    path('add/company/', views.addCompanyPage, name='addCompanyPage'),
]