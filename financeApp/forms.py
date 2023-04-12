from django import forms
from .models import Company, BalanceSheet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('companyName', )

class AddBalanceSheetForm(forms.ModelForm):
    class Meta:
        model = BalanceSheet
        fields = ('company', 'activeName', 'year', 'cash', 'accountsReceivable', 'inventory', 'prepaidExpenses', 'shortTermInvestments',
                  'longTermInvestments', 'propertyPlantEquipement', 'lessAccumulatedDepreciation', 'intangibleAssets', 'deferredIncomeTax',
                  'other', 'accountsPayable', 'shortTermLoans', 'incomeTaxes', 'accruedSalaries', 'unearnedRevenue', 'currentPortion',
                  'longTermDebt', 'defferedIncomeTax', 'otherLongTerm', 'ownerInvestment', 'retainedEarnings', 'otherOwnerInvestment'
                  )

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")