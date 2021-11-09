from django import forms
from django.db.models import query
from django.forms import fields
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    
    class Meta:
        model = Expense
        fields = '__all__'