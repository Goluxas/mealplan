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

		# The home page refreshes and there is an error message saying
		# that entree names cannot be blank

		# She tries again with some text for the item which now works

		# Perversely, she now decides to submit a second blank entree name

		# She receives a similar warning on the arsenal page

		# And she can correct it by filling some text in
		self.fail('write me!')
