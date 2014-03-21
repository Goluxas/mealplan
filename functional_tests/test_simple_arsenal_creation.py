import sys
import unittest
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):

	def test_can_start_adding_entrees_and_view_them_later(self):
		# Mallory wants to add a new entree that she learned how to cook.
		# She fires up her browser and navigates to the MealPlan site.
		self.browser.get(self.server_url)

		# Mallory notices page title and header mention MealPlan
		self.assertIn('MealPlan', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('MealPlan', header_text)

		# Mallory is presented with the option to add an entree right away
		inputbox = self.get_entree_input_box()
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter an entree'
		)

		# Mallory types "Cheese Omelette" into the text box
		inputbox.send_keys('Cheese Omelette')

		# Mallory hits enter, page updates and now lists
		# "Cheese Omelette (entree)"
		inputbox.send_keys(Keys.ENTER)
		mallory_meals_url = self.browser.current_url
		self.assertRegex(mallory_meals_url, '/meals/.+')
		self.check_for_row_in_entree_table('Cheese Omelette (entree)')

		# Text box remains. Mallory also types "Chicken Fajitas" and confirms.
		inputbox = self.get_entree_input_box()
		inputbox.send_keys('Chicken Fajitas')
		inputbox.send_keys(Keys.ENTER)

		# Page updates, now shows both Cheese Omelette and
		# "Chicken Fajitas (entree)"
		self.check_for_row_in_entree_table('Cheese Omelette (entree)')
		self.check_for_row_in_entree_table('Chicken Fajitas (entree)')

		# A second user, Scott, comes to the site

		## New browser session to ensure that nothing from Mallory gets through
		self.browser.quit()
		self.browser = webdriver.Chrome()

		# Scott visits the home page. There's no sign of Mallory's meals.
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Cheese Omelette', page_text)
		self.assertNotIn('Chicken Fajitas', page_text)

		# Scott enters his first entree, starting a new meal collection
		inputbox = self.get_entree_input_box()
		inputbox.send_keys('PB&J')
		inputbox.send_keys(Keys.ENTER)

		# Scott gets his own unique URL
		scott_meals_url = self.browser.current_url
		self.assertRegex(scott_meals_url, '/meals/.+')
		self.assertNotEqual(scott_meals_url, mallory_meals_url)

		# Again there's no sign of Mallory's meals
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Cheese Omelette', page_text)
		self.assertIn('PB&J', page_text)

		# Satisfied, user closes browser.
