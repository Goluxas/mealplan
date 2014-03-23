from django.db import models
from django.core.urlresolvers import reverse

class Arsenal(models.Model):
	
	def get_absolute_url(self):
		return reverse('view_arsenal', args=[self.id])

class Entree(models.Model):
	name = models.TextField()
	arsenal = models.ForeignKey(Arsenal)

	class Meta:
		unique_together = ('arsenal', 'name')

	def __str__(self):
		return self.name
