from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

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


class EntreeAndArsenalModelTest(TestCase):

	def test_saving_and_retrieving_entrees(self):
		arsenal = Arsenal()
		arsenal.save()

		first_entree = Entree()
		first_entree.name = 'The first (ever) entree'
		first_entree.arsenal = arsenal
		first_entree.save()

		second_entree = Entree()
		second_entree.name = 'Second entree'
		second_entree.arsenal = arsenal
		second_entree.save()

		saved_arsenal = Arsenal.objects.first()
		self.assertEqual(saved_arsenal, arsenal)

		saved_entrees = Entree.objects.all()
		self.assertEqual(saved_entrees.count(), 2)

		first_saved_entree = saved_entrees[0]
		second_saved_entree = saved_entrees[1]
		self.assertEqual(first_saved_entree.name, 'The first (ever) entree')
		self.assertEqual(first_saved_entree.arsenal, arsenal)
		self.assertEqual(second_saved_entree.name, 'Second entree')
		self.assertEqual(second_saved_entree.arsenal, arsenal)


class MealsViewTest(TestCase):

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


class NewMealsTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/meals/new', data={'entree_name': 'A new entree name'})

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'A new entree name')

	def test_redirects_after_POST(self):
		response = self.client.post('/meals/new', data={'entree_name': 'A new entree name'})
		new_ars = Arsenal.objects.first()

		self.assertRedirects(response, '/meals/%d/' % (new_ars.id))


class NewEntreeTest(TestCase):

	def test_can_save_a_POST_request_to_an_existsing_arsenal(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()

		self.client.post('/meals/%d/new_entree' % (correct_ars.id),
				data={'entree_name': 'New entree for existing Arsenal'}
		)

		self.assertEqual(Entree.objects.count(), 1)
		new_entree = Entree.objects.first()
		self.assertEqual(new_entree.name, 'New entree for existing Arsenal')
		self.assertEqual(new_entree.arsenal, correct_ars)

	def test_redirects_to_meals_view(self):
		other_ars = Arsenal.objects.create()
		correct_ars = Arsenal.objects.create()

		response = self.client.post('/meals/%d/new_entree' % (correct_ars.id),
				data={'entree_name': 'New entree for existing Arsenal'}
		)

		self.assertRedirects(response, '/meals/%d/' % (correct_ars.id))
