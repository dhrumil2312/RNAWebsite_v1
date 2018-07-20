from django.db import models

class UserInput(models.Model):
    id = models.AutoField(primary_key=True)
    inputText = models.CharField(max_length=5000)
    structure = models.CharField(max_length=5000)
    timestamp = models.DateTimeField()


class Results(models.Model):
    input_id = models.IntegerField()
    result = models.CharField(max_length=5000)
    timestamp = models.DateTimeField()

class Entrna_Resutls(models.Model):
    sequence = models.CharField(max_length=5000)
    structure = models.CharField(max_length=5000)
    foldability = models.FloatField()
    e = models.FloatField()
    mf = models.FloatField()
    mf_s = models.CharField(max_length=5000)


class QLRNA_Input(models.Model):
    id = models.AutoField(primary_key=True)
    structure = models.CharField(max_length=5000)
    emailId = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()
