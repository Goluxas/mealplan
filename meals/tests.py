from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from meals.views import home_page
from meals.models import Entree

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['entree_name'] = 'A new entree name'

		response = home_page(request)

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'A new entree name')

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['entree_name'] = 'A new entree name'

		response = home_page(request)

		self.assertEqual(response.status_code, 302) #redirect
		self.assertEqual(response['location'], '/')

	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()

		home_page(request)

		self.assertEqual(Entree.objects.count(), 0)

	def test_home_page_displays_all_list_items(self):
		Entree.objects.create(name='ent1')
		Entree.objects.create(name='ent2')

		request = HttpRequest()
		response = home_page(request)

		self.assertIn('ent1', response.content.decode())
		self.assertIn('ent2', response.content.decode())
		

class EntreeModelTest(TestCase):

	def test_saving_and_retrieving_entrees(self):
		first_entree = Entree()
		first_entree.name = 'The first (ever) entree'
		first_entree.save()

		second_entree = Entree()
		second_entree.name = 'Second entree'
		second_entree.save()

		saved_entrees = Entree.objects.all()
		self.assertEqual(saved_entrees.count(), 2)

		first_saved_entree = saved_entrees[0]
		second_saved_entree = saved_entrees[1]
		self.assertEqual(first_saved_entree.name, 'The first (ever) entree')
		self.assertEqual(second_saved_entree.name, 'Second entree')
