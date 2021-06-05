from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from notes.models import Note


class ShopCart(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL, null= True)
    note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.note.title