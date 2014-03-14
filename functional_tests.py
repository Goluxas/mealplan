import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_adding_entrees_and_view_them_later(self):
		# User wants to add a new entree that they learned how to cook.
		# They fire up their browser and navigate to the MealPlan site.
		self.browser.get('http://localhost:8000')

		# User notices page title and header mention MealPlan
		self.assertIn('MealPlan', self.browser.title)

		# User is presented with the option to add an entree right away

		# User types "Cheese Omelette" into the text box

		# When user hits enter, page updates and now lists
		# "Cheese Omelette (entree)"

		# Text box remains. User also types "Chicken Fajitas" and confirms.

		# Page updates, now shows both Cheese Omelette and
		# "Chicken Fajitas (entree)"

		# User wonders if they can get back to this later. Some text on the
		# page mentions that a unique URL has been generated to allow that.

		# User visits that URL, confirms it indeed stored the food items.

		self.fail('Finish the test!')
		# Satisfied, user closes browser.

if __name__ == '__main__':
	unittest.main()
