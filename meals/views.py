from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
	return render(request, 'home.html', {
				'new_entree_name': request.POST.get('entree_name', ''),
			})
