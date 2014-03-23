from django.test import TestCase
from django.core.exceptions import ValidationError

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

	def test_cannot_save_empty_entrees(self):
		ars = Arsenal.objects.create()
		entree = Entree(arsenal=ars, name='')
		with self.assertRaises(ValidationError):
			entree.save()
			entree.full_clean()

	def test_get_absolute_url(self):
		ars = Arsenal.objects.create()
		
		self.assertEqual(ars.get_absolute_url(), '/meals/%d/' % (ars.id))

	def test_duplicate_entrees_are_invalid(self):
		ars = Arsenal.objects.create()
		Entree.objects.create(arsenal=ars, name='test')
		with self.assertRaises(ValidationError):
			entree = Entree(arsenal=ars, name='test')
			entree.full_clean()

	def test_CAN_save_same_item_to_different_arsenal(self):
		ars1 = Arsenal.objects.create()
		ars2 = Arsenal.objects.create()
		Entree.objects.create(arsenal=ars1, name='test')
		entree = Entree(arsenal=ars2, name='test')
		entree.full_clean() # should not raise

	def test_string_representation(self):
		entree = Entree(name='test')
		self.assertEqual(str(entree), 'test')
