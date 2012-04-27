from django.db import models
from django.forms import ModelForm
import datetime
# Create your models here.

class Poem(models.Model):
    name = models.CharField(max_length=250)
    circularity = models.IntegerField()
    disruption = models.IntegerField()
    sound = models.IntegerField()
    semantics = models.IntegerField()
    pub_date = models.DateTimeField('Published on')
    
    def __unicode__(self):
        return self.name
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    
    was_published_today.short_description = 'Published Today?'
    
class Author(models.Model):
    poem = models.ForeignKey(Poem)
    first = models.CharField(max_length=250)
    last = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.first + " " + self.last
    
class PoemForm(ModelForm): 
    class Meta:
        model = Poem   