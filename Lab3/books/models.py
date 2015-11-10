from django.db import models

# Create your models here.
    
class Author(models.Model):
    AuthorID  = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=45,unique=True)
    Age = models.IntegerField()
    Country = models.CharField(max_length=45)
    
class book(models.Model):
    ISBN = models.CharField(max_length=13,primary_key=True)
    Title = models.CharField(max_length=45)
    AuthorID = models.ForeignKey(Author,null=True)
    Publisher = models.CharField(max_length=45)
    PublishDate = models.DateField()
    Price = models.FloatField()
    