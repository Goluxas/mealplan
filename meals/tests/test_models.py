from django.test import TestCase

from meals.models import Entree, Arsenal

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
