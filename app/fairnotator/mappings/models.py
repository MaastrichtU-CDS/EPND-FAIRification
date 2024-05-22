from django.db import models

class Datasource(models.Model):
    name = models.CharField(max_length=255)

class CsvFile(Datasource):
    filename = models.CharField(max_length=255)

class Database(Datasource):
    name = models.CharField(max_length=255)
    schema = models.CharField(max_length=255)

class Table(models.Model):
    name = models.CharField(max_length=255)
    datasource = models.ForeignKey(Datasource, on_delete=models.CASCADE)

class Column(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    nullable = models.BooleanField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class ForeignKey(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    references = models.ForeignKey(Column, on_delete=models.CASCADE)

class Mapping(models.Model):
    name = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class Source(models.Model):
    name = models.CharField(max_length=255)
    mapping = models.OneToOneField(Mapping, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

class Unit(models.Model):
    name = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)

class Target(models.Model):
    name = models.CharField(max_length=255)
    mapping = models.OneToOneField(Mapping, on_delete=models.CASCADE)
    uri = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

