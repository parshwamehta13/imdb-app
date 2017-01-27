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


class Actor (models.Model):
	id = models.CharField(primary_key=True,max_length=100)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=20)
	biography = models.TextField()
	image = models.URLField()
	birth_notes = models.TextField()
	movie_list = models.TextField()
	birthday = models.CharField(max_length=100,default="1st January 1990")

	def __unicode__(self):
		return self.name

class Actor_Graph (models.Model):
	id = models.CharField(primary_key=True,max_length=100)
	json_data = models.TextField()

