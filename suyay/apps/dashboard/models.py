from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
       return 'Hospital: ' + self.name

class Ambiente(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)

    def __str__(self):
       return 'Ambiente: ' + self.name

class Respirador(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=250)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
       return 'Respirador: ' + self.code
