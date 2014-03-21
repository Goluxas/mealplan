from django import forms

from meals.models import Entree


EMPTY_ENTREE_ERROR = 'Entree names must not be blank'

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
