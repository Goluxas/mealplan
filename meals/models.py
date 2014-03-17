from django.db import models

class Arsenal(models.Model):
	pass

class Entree(models.Model):
	name = models.TextField()
	arsenal = models.ForeignKey(Arsenal)
