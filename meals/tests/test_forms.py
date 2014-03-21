from django.test import TestCase

from meals.forms import EntreeForm, EMPTY_ENTREE_ERROR


class EntreeFormTest(TestCase):

	def test_form_entree_input_has_placeholder_and_css_classes(self):
		form = EntreeForm()

		self.assertIn('placeholder="Enter an entree"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_entrees(self):
		form = EntreeForm(data={'name': ''})

		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['name'], [EMPTY_ENTREE_ERROR])
