from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Journal(models.Model):
	user = models.ForeignKey(User)
 	mapurl = models.URLField()

class Entry(models.Model):
	journal = models.ForeignKey(Journal)
	timestamp = models.DateTimeField()
	class Meta:
		abstract = True

class TextEntry(Entry):
	text = models.TextField(blank=True)

	def __unicode__(self):
		return
