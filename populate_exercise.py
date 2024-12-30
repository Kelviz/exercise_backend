import os
import django
import requests
from django.core.files.base import ContentFile
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercise_backend.settings')
django.setup()
import requests
from exercise.models import *



def get_equipments():
        url = "https://exercisedb.p.rapidapi.com/exercises/equipmentList"

        headers = {
                "x-rapidapi-key": "40d0cc352dmshc7f2620671de911p16ad36jsn03214c14f1a6",
                "x-rapidapi-host": "exercisedb.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        equipment_list = response.json()
        print(response.json())

        for equipment in equipment_list:
                equipment_exist = Equipment.objects.filter(name=equipment).exists()
                if equipment_exist:
                        print('equipment exists')
                        pass
                else:
                        new_equipment = Equipment(
                                name = equipment
                        )

                        new_equipment.save()
                        print(f'{new_equipment.name} saved to database')

        


def get_bodyparts():
        url = "https://exercisedb.p.rapidapi.com/exercises/bodyPartList"

        headers = {
                "x-rapidapi-key": "40d0cc352dmshc7f2620671de911p16ad36jsn03214c14f1a6",
                "x-rapidapi-host": "exercisedb.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        bodypart_list = response.json()

        print(response.json())

        for equipment in bodypart_list:
                equipment_exist = BodyPart.objects.filter(name=equipment).exists()
                if equipment_exist:
                        print('equipment exists')
                        pass
                else:
                        new_equipment = BodyPart(
                                name = equipment
                        )

                        new_equipment.save()
                        print(f'{new_equipment.name} saved to database')



def exercises():
        url = "https://exercisedb.p.rapidapi.com/exercises"

        querystring = {"limit":"15","offset":"0"}

        headers = {
                "x-rapidapi-key": "40d0cc352dmshc7f2620671de911p16ad36jsn03214c14f1a6",
                "x-rapidapi-host": "exercisedb.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(response.json())

        exercise_list = response.json()

        for x in exercise_list:
                name = x['name']
                get_bodypart =  x['bodyPart']
                get_equipment = x['equipment']
                imageUrl = x['gifUrl']
                get_target = x['target']
                secondaryMuscles = x['secondaryMuscles']
                instructions = x['instructions']

                body_part = BodyPart.objects.filter(name=get_bodypart).first()
                equipment = Equipment.objects.filter(name=get_equipment).first()
                target = Target.objects.filter(name=get_target).first()




                exercise_exist = Exercise.objects.filter(name=name).first()
                if exercise_exist:
                        print('exercise exists')
                        try:
                                response = requests.get(imageUrl, stream=True)
                                if response.status_code == 200:
                                        # Get the image content
                                        #file_name = imageUrl.split("/")[-1]
                                        img_name = f"{name}.gif"
                                        exercise_exist.image.save(img_name, ContentFile(response.content), save=True)
                                        print(f"Image successfully saved for {exercise_exist.name}.")
                                else:
                                        print(f"Failed to download image. Status code: {response.status_code}")
                        except Exception as e:
                                print(f"Error occurred while downloading the image: {e}")

                        print(f'{exercise_exist.name} saved to database')
                else:

                        


                        new_exercise = Exercise(
                                name = name,
                                bodypart = body_part,
                                equipment=equipment,
                                target=target,
                                secondary_muscles = secondaryMuscles,
                                instructions=instructions

                        )

                        new_exercise.save()

                        try:
                                response = requests.get(imageUrl, stream=True)
                                if response.status_code == 200:
                                        # Get the image content
                                        #file_name = imageUrl.split("/")[-1]
                                        img_name = f"{name}.gif"
                                        new_exercise.image.save(img_name, ContentFile(response.content), save=True)
                                        print(f"Image successfully saved for {new_exercise.name}.")
                                else:
                                        print(f"Failed to download image. Status code: {response.status_code}")
                        except Exception as e:
                                print(f"Error occurred while downloading the image: {e}")

                        print(f'{new_exercise.name} saved to database')



def get_targets():
        url = "https://exercisedb.p.rapidapi.com/exercises/targetList"

        headers = {
                "x-rapidapi-key": "40d0cc352dmshc7f2620671de911p16ad36jsn03214c14f1a6",
                "x-rapidapi-host": "exercisedb.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        target_list = response.json()

        print(response.json())

        for equipment in target_list:
                equipment_exist = Target.objects.filter(name=equipment).exists()
                if equipment_exist:
                        print('equipment exists')
                        pass
                else:
                        new_equipment = Target(
                                name = equipment
                        )

                        new_equipment.save()
                        print(f'{new_equipment.name} saved to database')




if __name__ == "__main__":
        #get_equipments()
        #get_bodyparts()
        #get_targets()
        exercises()
