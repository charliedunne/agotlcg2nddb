from django.db import models

# Serializers
from rest_framework import serializers

# Create your models here.
class Cycle(models.Model):
    short = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.short

class Pack(models.Model):
    short = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)

    def __str__(self):
        return self.short

class Faction(models.Model):
    short = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.short

class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class Card(models.Model):
    code = models.CharField(max_length=5, unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unique = models.BooleanField()
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)
    loyal = models.BooleanField()
    cost = models.CharField(max_length=2, blank=True, null=True)
    iMilitary = models.BooleanField(blank=True, null=True)
    iIntrigue = models.BooleanField(blank=True, null=True)
    iPower = models.BooleanField(blank=True, null=True)
    strenght = models.CharField(max_length=2, blank=True, null=True)
    traits = models.ManyToManyField(Trait, blank=True)
    illustrator = models.CharField(max_length=50, blank=True, null=True)
    decklimit = models.PositiveIntegerField()
    text = models.TextField(blank=True, null=True)
    flavor = models.TextField(blank=True, null=True)
    pIncome = models.CharField(max_length=2, blank=True, null=True)
    pInitiative = models.CharField(max_length=2, blank=True, null=True)
    pClaim = models.CharField(max_length=2, blank=True, null=True)
    pReserve = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.code

class Language(models.Model):
    short = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.short

class TranslateCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    text = models.TextField(blank=True, null=True)
    flavor = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code

class TranslateFaction(models.Model):
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class TranslateTrait(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name   

class TranslatePack(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name             

class TranslateCycle(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name           