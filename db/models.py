from atexit import register
from django.db import models

from django import template

register = template.Library()

# Serializers
from rest_framework import serializers

# Translation for Type
def type_es(name):
    match name:
        case "Character":
            return "Personaje"
        case "Event":
            return "Evento"
        case "Attachment":
            return "Accesorio"
        case "Plot":
            return "Trama"
        case "Location":
            return "Localización"
        case "Title":
            return "Título"
        case _:
            return name

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

    def getColorBg(self):
        match self.faction.short:
            case "baratheon":
                return "rgb(230, 200, 50)"
            case "lannister":
                return "rgb(230, 30, 30)"
            case "targaryen":
                return "black"
            case "martell":
                return "orange"
            case "tyrell":
                return "green"
            case "thenightswatch":
                return "grey"
            case "greyjoy":
                return "rgb(60, 50, 200)"
            case "stark":
                return "white"
            case "neutral":
                return "brown"
            case _:
                return ""

    def getColorFg(self):
        match self.faction.short:
            case "baratheon":
                return "black"
            case "lannister":
                return "black"
            case "targaryen":
                return "White"
            case "martell":
                return "black"
            case "tyrell":
                return "black"
            case "thenightswatch":
                return "black"
            case "greyjoy":
                return "white"
            case "stark":
                return "black"
            case "neutral":
                return "black"
            case _:
                return ""


    def isCharacter(self):
        if self.type.name == "Character":
            return True
        else:
            return False

    def isPlot(self):
        if self.type.name == "Plot":
            return True
        else:
            return False
    
    def isLocation(self):
        if self.type.name == "Location":
            return True
        else:
            return False

    def getTraits_es(self):
        lg = Language.objects.all().get(short='es')
        
        outString = ""

        for trait in self.traits.all():
            try:
                translation = TranslateTrait.objects.all().get(trait=trait, language=lg)
            except:
                pass

            if 'translation' in locals():
                outString = outString + translation.name + ". "
            else:
                outString = outString + trait.name + ". "

        return outString

    def getFaction_es(self):
        lg = Language.objects.all().get(short='es')
        translation = TranslateFaction.objects.all().get(faction=self.faction, language=lg)
   
        return translation.name

    def getLoyal_es(self):

        if self.loyal == True:
            return "Leal"
        else:
            return "No Leal"

    def getType_es(self):

        return type_es(self.type.name)

    def getFactionCode(self):
        return self.faction

    def getName_es(self):
        lg = Language.objects.all().get(short='es')
        try:
            translation = TranslateCard.objects.all().get(card=self, language=lg)
        except:
            pass

        if 'translation' in locals():
            name = translation.name
        else:
            name = self.name + '*'

        return name

    def getName(self, lang):
        try:
            lg = Language.objects.all().get(short=lang)
            translation = TranslateCard.objects.all().get(card=self, language=lg)
        except:
            pass

        if translation is not None:
            name = translation.name
        else:
            name = self.name

        return name

    def getText_es(self):
        lg = Language.objects.all().get(short='es')
        try:
            translation = TranslateCard.objects.all().get(card=self, language=lg)
        except:
            pass

        if 'translation' in locals():
            text = translation.text
        else:
            text = self.name + '*'

        return text

    def getFlavor_es(self):
        lg = Language.objects.all().get(short='es')
        try:
            translation = TranslateCard.objects.all().get(card=self, language=lg)
        except:
            pass

        if 'translation' in locals():
            flavor = translation.flavor
        else:
            flavor = self.name + '*'

        return flavor 

    @register.simple_tag
    def theName(card, lang):
        return Card.getName(lang)

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

