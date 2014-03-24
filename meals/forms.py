from django import forms
from django.core.exceptions import ValidationError

from meals.models import Entree


EMPTY_ENTREE_ERROR = 'Entree names must not be blank'
DUPLICATE_ENTREE_ERROR = 'Entree already added'

class EntreeForm(forms.models.ModelForm):

	class Meta:
		model = Entree 
		fields = ('name',)
		widgets = {
			'name': forms.fields.TextInput(
				attrs={
					'placeholder': 'Enter an entree',
					'class': 'form-control input-lg',
				}),
			}

		error_messages = {
				'name': {'required': EMPTY_ENTREE_ERROR},
			}

	def save(self, for_arsenal):
		self.instance.arsenal = for_arsenal
		return super().save()


class ExistingArsenalEntreeForm(EntreeForm):

	def __init__(self, for_arsenal, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.arsenal = for_arsenal

	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'name': [DUPLICATE_ENTREE_ERROR]}
			self._update_errors(e)
