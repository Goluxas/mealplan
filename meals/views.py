from django.shortcuts import render, redirect
from django.http import HttpResponse

from meals.models import Entree

def home_page(request):
	if request.method == 'POST':
		Entree.objects.create(name=request.POST['entree_name'])
		return redirect('/meals/the-only-mealplan-in-the-world')

	return render(request, 'home.html')

def view_meals(request):
	return render(request, 'meals.html', {
				'entrees': Entree.objects.all(),
			})
