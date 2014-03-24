from django.test import TestCase
from django.core.exceptions import ValidationError

from meals.models import Entree, Arsenal

class EntreeModelTest(TestCase):

	def test_default_name(self):
		entree = Entree()
		self.assertEqual(entree.name, '')

	def test_entree_is_related_to_list(self):
		ars = Arsenal.objects.create()
		entree = Entree()
		entree.arsenal = ars
		entree.save()
		self.assertIn(entree, ars.entree_set.all())

	def test_arsenal_ordering(self):
		ars = Arsenal.objects.create()
		ent1 = Entree.objects.create(name='1', arsenal=ars)
		ent2 = Entree.objects.create(name='2', arsenal=ars)
		ent3 = Entree.objects.create(name='3', arsenal=ars)

		self.assertEqual(list(Entree.objects.all()), [ent1, ent2, ent3])

	def test_cannot_save_empty_entrees(self):
		ars = Arsenal.objects.create()
		entree = Entree(arsenal=ars, name='')
		with self.assertRaises(ValidationError):
			entree.save()
			entree.full_clean()

	def test_duplicate_entrees_are_invalid(self):
		ars = Arsenal.objects.create()
		Entree.objects.create(arsenal=ars, name='test')
		with self.assertRaises(ValidationError):
			entree = Entree(arsenal=ars, name='test')
			entree.full_clean()
			#entree.save()

	def test_CAN_save_same_entree_to_different_arsenal(self):
		ars1 = Arsenal.objects.create()
		ars2 = Arsenal.objects.create()
		Entree.objects.create(arsenal=ars1, name='test')
		entree = Entree(arsenal=ars2, name='test')
		entree.full_clean() # should not raise

	def test_string_representation(self):
		entree = Entree(name='test')
		self.assertEqual(str(entree), 'test')

class ArsenalModelTest(TestCase):

	def test_get_absolute_url(self):
		ars = Arsenal.objects.create()
		
		self.assertEqual(ars.get_absolute_url(), '/meals/%d/' % (ars.id))
