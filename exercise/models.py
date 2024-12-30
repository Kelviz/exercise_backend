from django.db import models

class BodyPart(models.Model):
        name = models.CharField(max_length=2000)

        def __str__(self):
                return self.name
        
        

class Equipment(models.Model):
        name = models.CharField(max_length=2000)

        def __str__(self):
                return self.name
        
        

class Target(models.Model):
        name = models.CharField(max_length=2000)

        def __str__(self):
                return self.name
        


class Exercise(models.Model):
        name = models.CharField(max_length=5000)
        equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
        bodypart = models.ForeignKey(BodyPart, on_delete=models.SET_NULL, null=True)
        target = models.ForeignKey(Target, on_delete=models.SET_NULL, null=True)
        image = models.ImageField(upload_to='images', blank=True, null=True)
        secondary_muscles = models.JSONField(default=list)
        instructions = models.JSONField(default=list)


        def __str__(self):
                return self.name
