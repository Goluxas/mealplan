from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from meals.models import Entree, Arsenal

def home_page(request):
	return render(request, 'home.html')

def view_arsenal(request, arsenal_id):
	ars = Arsenal.objects.get(id=arsenal_id)
	if request.method == 'POST':
		Entree.objects.create(name=request.POST['entree_name'], arsenal=ars)
		return redirect('/meals/%d/' % (ars.id))
	return render(request, 'arsenal.html', {
				'arsenal': ars,
			})

def new_arsenal(request):
	ars = Arsenal.objects.create()
	entree = Entree(name=request.POST['entree_name'], arsenal=ars)
	try:
		entree.full_clean()
		entree.save()
	except ValidationError:
		ars.delete()
		error = 'Entree names must not be blank'
		return render(request, 'home.html', {'error':error})
	return redirect('/meals/%d/' % (ars.id))
