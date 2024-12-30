from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *


router = routers.DefaultRouter()


# Schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Exercise API",
        default_version='v1',
        description="""The ExerciseDB API is a versatile and detailed resource, offering access to over 1,300 exercises
          categorized by body part, target muscle group, and required equipment. Each exercise is paired with high-quality
            animations demonstrating proper form and movement, making it easy to understand and execute with precision.
              This API is perfect for developers crafting fitness apps, trainers designing custom workout programs, and
                fitness enthusiasts looking for clear and accurate exercise instructions. With its intuitive and well-organized 
                structure, the ExerciseDB API ensures effortless integration and efficient access to comprehensive exercise data..""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)



router.register('equipment-list', EquipmentViewset, basename='equipment-list')
router.register('body-list', BodyPartViewset, basename='body-list')
router.register('target-list', TargetViewset, basename='target-list')
router.register('exercises', ExerciseViewset, basename='exercises')

urlpatterns = [
        
        path('v1/exercises/search/', SearchExerciseView.as_view(), name='exercise-search'),
        path('v1/', include(router.urls)),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]