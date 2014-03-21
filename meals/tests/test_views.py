from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from meals.views import home_page
from meals.models import Entree, Arsenal

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)


class ArsenalViewTest(TestCase):

	def test_uses_meals_template(self):
		ars = Arsenal.objects.create()
		response = self.client.get('/meals/%d/' % (ars.id))
		self.assertTemplateUsed(response, 'arsenal.html')

	def test_displays_only_meals_for_that_arsenal(self):
		correct_ars = Arsenal.objects.create()
		Entree.objects.create(name='ent1', arsenal=correct_ars)
		Entree.objects.create(name='ent2', arsenal=correct_ars)
		wrong_ars = Arsenal.objects.create()
		Entree.objects.create(name='other ent1', arsenal=wrong_ars)
		Entree.objects.create(name='other ent2', arsenal=wrong_ars)

		response = self.client.get('/meals/%d/' % (correct_ars.id))

		self.assertContains(response, 'ent1')
		self.assertContains(response, 'ent2')
		self.assertNotContains(response, 'other ent1')
		self.assertNotContains(response, 'other ent2')

	def test_passes_correct_arsenal_to_template(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()
		response = self.client.get('/meals/%d/' % (correct_ars.id))
		self.assertEqual(response.context['arsenal'], correct_ars)

	def test_can_save_a_POST_request_to_an_existsing_arsenal(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()

		self.client.post('/meals/%d/' % (correct_ars.id),
				data={'entree_name': 'New entree for existing Arsenal'}
		)

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'New entree for existing Arsenal')
		self.assertEqual(new_entree.arsenal, correct_ars)

	def test_POST_redirects_to_arsenal_view(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()

		response = self.client.post('/meals/%d/' % (correct_ars.id),
				data={'entree_name': 'New entree for existing Arsenal'}
		)

		self.assertRedirects(response, '/meals/%d/' % (correct_ars.id))

	def test_validation_errors_end_up_on_arsenal_page(self):
		ars = Arsenal.objects.create()
		response = self.client.post('/meals/%d/' % (ars.id),
									data={'entree_name': ''})

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'arsenal.html')
		expected_error = escape('Entree names must not be blank')
		self.assertContains(response, expected_error)


class NewArsenalTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/meals/new', data={'entree_name': 'A new entree name'})

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'A new entree name')

	def test_redirects_after_POST(self):
		response = self.client.post('/meals/new', data={'entree_name': 'A new entree name'})
		new_ars = Arsenal.objects.first()

		self.assertRedirects(response, '/meals/%d/' % (new_ars.id))

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/meals/new', data={'entree_name':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape('Entree names must not be blank')
		self.assertContains(response, expected_error)

	def test_invalid_entrees_are_not_saved(self):
		self.client.post('/meals/new', data={'entree_name':''})
		self.assertEqual(Arsenal.objects.count(), 0)
		self.assertEqual(Entree.objects.count(), 0)
