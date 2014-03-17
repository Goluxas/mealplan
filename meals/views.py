from django.shortcuts import render, redirect
from django.http import HttpResponse

from meals.models import Entree, Arsenal

def home_page(request):
	return render(request, 'home.html')

def view_arsenal(request, arsenal_id):
	ars = Arsenal.objects.get(id=arsenal_id)
	return render(request, 'arsenal.html', {
				'arsenal': ars,
			})

def new_arsenal(request):
	ars = Arsenal.objects.create()
	Entree.objects.create(name=request.POST['entree_name'], arsenal=ars)
	return redirect('/meals/%d/' % (ars.id))

def add_entree(request, arsenal_id):
	ars = Arsenal.objects.get(id=arsenal_id)
	Entree.objects.create(name=request.POST['entree_name'], arsenal=ars)
	return redirect('/meals/%d/' % (ars.id))
