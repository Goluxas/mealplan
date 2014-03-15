from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from meals.views import home_page

class SmokeTest(TestCase):
	
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

		self.assertIn('A new entree name', response.content.decode())
		expected_html = render_to_string(
				'home.html',
				{'new_entree_name': 'A new entree name'}
		)
		self.assertEqual(response.content.decode(), expected_html)
