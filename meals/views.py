from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from meals.models import Entree, Arsenal
from meals.forms import EntreeForm

def home_page(request):
	return render(request, 'home.html', {'form': EntreeForm()})

def view_arsenal(request, arsenal_id):
	ars = Arsenal.objects.get(id=arsenal_id)
	form = EntreeForm()

	if request.method == 'POST':
		form = EntreeForm(request.POST)
		if form.is_valid():
			Entree.objects.create(name=request.POST['name'], arsenal=ars)
			return redirect(ars)

	return render(request, 'arsenal.html', {
				'arsenal': ars,
				'form': form,
			})

def new_arsenal(request):
	form = EntreeForm(data=request.POST)
	if form.is_valid():
		ars = Arsenal.objects.create()
		Entree.objects.create(name=request.POST['name'], arsenal=ars)
		return redirect(ars)
	else:
		return render(request, 'home.html', {'form':form})
