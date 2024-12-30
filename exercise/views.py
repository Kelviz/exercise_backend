import logging
import hashlib
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'message': 'Data fetched successfully',
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
            }
        })



class EquipmentViewset(viewsets.ModelViewSet):
        queryset = Equipment.objects.all()
        serializer_class = EquipmentSerializer


class BodyPartViewset(viewsets.ModelViewSet):
        queryset = BodyPart.objects.all()
        serializer_class = BodyPartSerializer
                                                                                                          


class TargetViewset(viewsets.ModelViewSet):
        queryset = Target.objects.all()
        serializer_class = TargetSerializer




class ExerciseViewset(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    pagination_class = CustomPagination
    cache_key_list = 'exercise_list'
    cache_key_detail = 'exercise_detail_{}'


    def get_queryset(self):
        queryset = Exercise.objects.all()
        equipment_query = self.request.query_params.get('equipment', None)
        body_part_query = self.request.query_params.get('bodyPart', None)
        target_query = self.request.query_params.get('target', None)

        if equipment_query is not None:
            equipment = Equipment.objects.filter(name=equipment_query).first()
            queryset = queryset.filter(equipment=equipment)

        if body_part_query is not None:
            body_part = BodyPart.objects.filter(name=body_part_query).first()
            queryset = queryset.filter(bodypart=body_part)

        if target_query is not None:
            print(f'query:{target_query}')
            target = Target.objects.filter(name=target_query).first()
            queryset = queryset.filter(target=target)

        return queryset

    def _generate_cache_key(self, prefix, request=None, **kwargs):
        """Generates a dynamic cache key."""

        # For `retrieve` method
        if 'pk' in kwargs:  
            return prefix.format(kwargs['pk'])

        # For `list` method (include query params)
        query_string = request.META.get('QUERY_STRING', '')
        hashed_query = hashlib.md5(query_string.encode()).hexdigest()
        return f"{prefix}_{hashed_query}"
    


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'equipment', openapi.IN_QUERY,
                description="Equipment name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'bodyPart', openapi.IN_QUERY,
                description="Body Part name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'target', openapi.IN_QUERY,
                description="Target muscle group name",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        cache_key = self._generate_cache_key(self.cache_key_list, request=request)
        cached_response = cache.get(cache_key)
        print('caching mehn')
        if cached_response:
            logger.info(f"Cache hit for key: {cache_key}")
            return Response(cached_response, status=status.HTTP_200_OK)
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
                
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = {
                    'status': 'success',
                    'message': 'Exercises fetched successfully',
                    'data': serializer.data
                }

            cache.set(cache_key, data,  60 * 15)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching exercises: {e}")
            return Response({"error": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        cache_key = self._generate_cache_key(self.cache_key_detail, **kwargs)
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.info(f"Cache hit for key: {cache_key}")
            return Response(cached_response, status=status.HTTP_200_OK)

        try:
            id = kwargs.get('pk')
            logger.info(f"Fetching exercise details for id: {id}")
            exercise = get_object_or_404(Exercise, id=id)
            serializer = self.get_serializer(exercise)
            data = {
                'message': 'Exercise fetched successfully',
                'data': serializer.data,
                'status': 'successful',
            }

            cache.set(cache_key, data, 60 * 15)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching exercise detail: {e}")
            return Response({"error": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










from django.db.models import Q
from rest_framework.views import APIView


class SearchExerciseView(APIView):
    """
    View for searching exercises by equipment, body part, and target with a single query.
    """

    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)

        if not search_query:
            return Response(
                {"error": "Search query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(f"Search Query: {search_query}")
        

        # Filter related models by the search query
        equipment_matches = Equipment.objects.filter(name__icontains=search_query)
        body_part_matches = BodyPart.objects.filter(name__icontains=search_query)
        target_matches = Target.objects.filter(name__icontains=search_query)

        # Filter exercises based on the matches
        exercise_queryset = Exercise.objects.filter(
            Q(name__in=search_query) |
            Q(equipment__in=equipment_matches) |
            Q(bodypart__in=body_part_matches) |
            Q(target__in=target_matches)
        ).distinct()


        paginator = self.pagination_class()
        page = paginator.paginate_queryset(exercise_queryset, request)
        if page is not None:
            serializer = ExerciseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        

        serializer = ExerciseSerializer(exercise_queryset, many=True)
        return Response({
            "status": "success",
            "message": "Search results fetched successfully",
            "search": search_query,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    


