# REST Framework
from rest_framework import serializers

# DB Models
from . import models

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cycle
        fields = ['__all__']

class PackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pack
        fields = ['__all__']        

class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Faction
        fields = ['__all__']        

class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trait
        fields = ['__all__']        

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = ['__all__']        

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ['__all__']        
