from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Search (models.Model):
	search_term = models.CharField(max_length=100)
	attribute_category = (('movie','movie'),('actor','actor'))
	attribute = models.CharField(choices=attribute_category,default='movie',max_length=30)

	def __str__(self):
		return self.search_term

	class Meta:
		ordering = ['-id']