from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from meals.views import home_page
from meals.models import Entree, Arsenal
from meals.forms import EntreeForm, EMPTY_ENTREE_ERROR

class HomePageTest(TestCase):
	
	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_home_page_uses_entree_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], EntreeForm)


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
				data={'name': 'New entree for existing Arsenal'}
		)

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'New entree for existing Arsenal')
		self.assertEqual(new_entree.arsenal, correct_ars)

	def test_POST_redirects_to_arsenal_view(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()

		response = self.client.post('/meals/%d/' % (correct_ars.id),
				data={'name': 'New entree for existing Arsenal'}
		)

		self.assertRedirects(response, '/meals/%d/' % (correct_ars.id))

	def test_displays_entree_form(self):
		ars = Arsenal.objects.create()
		response = self.client.get('/meals/%d/' % (ars.id))
		
		self.assertIsInstance(response.context['form'], EntreeForm)
		self.assertContains(response, 'name="name"')

	def post_invalid_input(self):
		ars = Arsenal.objects.create()
		return self.client.post('/meals/%d/' % (ars.id), data={'name':''})

	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()

		self.assertEqual(Entree.objects.count(), 0)
	
	def test_for_invalid_input_renders_arsenal_template(self):
		response = self.post_invalid_input()

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'arsenal.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()

		self.assertIsInstance(response.context['form'], EntreeForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()

		self.assertContains(response, EMPTY_ENTREE_ERROR)

	from unittest import skip
	@skip
	def test_duplicate_entree_validation_errors_end_up_on_arsenal_page(self):
		ars = Arsenal.objects.create()
		ent = Entree.objects.create(name='test', arsenal=ars)
		response = self.client.post('/meals/%d/' % (ars.id),
									data={'name': 'test'})
		expected_error = escape('Entree already added')

		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'arsenal.html')
		self.assertEqual(Entree.objects.all().count(), 1)

class NewArsenalTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/meals/new', data={'name': 'A new entree name'})

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'A new entree name')

	def test_redirects_after_POST(self):
		response = self.client.post('/meals/new', data={'name': 'A new entree name'})
		new_ars = Arsenal.objects.first()

		self.assertRedirects(response, '/meals/%d/' % (new_ars.id))

	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/meals/new', data={'name':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		
	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/meals/new', data={'name':''})
		self.assertContains(response, EMPTY_ENTREE_ERROR)

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/meals/new', data={'name':''})
		self.assertIsInstance(response.context['form'], EntreeForm)

	def test_invalid_entrees_are_not_saved(self):
		self.client.post('/meals/new', data={'name':''})
		self.assertEqual(Arsenal.objects.count(), 0)
		self.assertEqual(Entree.objects.count(), 0)
