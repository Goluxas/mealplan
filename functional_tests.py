import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('MealPlan', header_text)

		# User is presented with the option to add an entree right away
		inputbox = self.browser.find_element_by_id('id_new_entree')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter an entree'
		)

		# User types "Cheese Omelette" into the text box
		inputbox.send_keys('Cheese Omelette')

		# When user hits enter, page updates and now lists
		# "Cheese Omelette (entree)"
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_entree_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
				any(row.text == 'Cheese Omelette' for row in rows),
				"New entree did not appear in table",
		)

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
