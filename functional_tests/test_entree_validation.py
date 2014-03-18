import sys
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

from .base import FunctionalTest

class EntreeValidationTest(FunctionalTest):

	def test_cannot_add_empty_entrees(self):
		# Mallory goes to the home page and accidentally tries to submit
		# an empty entree name. She hits enter on the empty input box
		self.browser.get(self.server_url)
		inputbox = self.browser.find_element_by_id('id_new_entree')
		inputbox.send_keys(Keys.ENTER)

		# The home page refreshes and there is an error message saying
		# that entree names cannot be blank
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'Entree names must not be blank')

		# She tries again with some text for the item which now works
		inputbox = self.browser.find_element_by_id('id_new_entree')
		inputbox.send_keys('some text\n')

		self.check_for_row_in_entree_table('some text (entree)')

		# Perversely, she now decides to submit a second blank entree name
		inputbox = self.browser.find_element_by_id('id_new_entree')
		inputbox.send_keys(Keys.ENTER)

		# She receives a similar warning on the arsenal page
		self.check_for_row_in_entree_table('some text (entree)')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'Entree names must not be blank')

		# And she can correct it by filling some text in
		inputbox = self.browser.find_element_by_id('id_new_entree')
		inputbox.send_keys('some different text\n')

		self.check_for_row_in_entree_table('some text (entree)')
		self.check_for_row_in_entree_table('some different text (entree)')
