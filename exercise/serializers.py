from rest_framework import serializers
from .models import *


class EquipmentSerializer(serializers.ModelSerializer):
        class Meta:
                model = Equipment
                fields = '__all__'


class BodyPartSerializer(serializers.ModelSerializer):
        class Meta:
                model = BodyPart
                fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):
        class Meta:
                model = Target
                fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
        equipment = EquipmentSerializer()
        bodypart = BodyPartSerializer()
        target = TargetSerializer()
        class Meta:
                model = Exercise
                fields = '__all__'