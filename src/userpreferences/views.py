from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.

def index(request, context = {}):

    exisits = UserPreference.objects.filter(user=request.user).exists()

    if exisits:
        preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':

        currency_data = []

        context['currencies'] = currency_data

        if exisits:
            context['preference'] = preference

        file_path = os.path.join(settings.BASE_DIR,'currencies.json')

        with open(file_path, 'r') as json_file:

            data = json.load(json_file)

        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})


        return render(request, 'preferences/index.html', context)

    else:
        currency = request.POST['currency']

        if exisits:
            preference.currency = currency
            preference.save()
            messages.success(request, 'Changes saved')
            return redirect('expenses')

        UserPreference.objects.create(user=request.user, currency=currency)

    return render (redirect, 'expenses')
