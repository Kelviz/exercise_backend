# Exercise API - README

## Overview

The **Exercise API** allows users to access a comprehensive library of exercises. Each exercise is equipped with metadata including body parts, equipment used, and target muscle groups. The API also supports query parameter filtering, enabling tailored exercise retrieval for specific needs.

### Features

- Filter exercises by equipment, body parts, and target muscle groups.
- Integration with caching for faster responses.
- OpenAPI documentation using **drf-yasg** for seamless developer experience.

---

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Django 3.2+
- Django Rest Framework (DRF)
- drf-yasg for OpenAPI documentation

### Setup Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Base URL:

`http://<server-domain>/api/v1/exercises/`

### Endpoints

| Method | Endpoint | Description          |
| ------ | -------- | -------------------- |
| GET    | `/`      | List all exercises   |
| GET    | `/{id}/` | Retrieve an exercise |

### Query Parameters for Filtering

| Parameter   | Type   | Description                  |
| ----------- | ------ | ---------------------------- |
| `equipment` | String | Filter by equipment name     |
| `bodyPart`  | String | Filter by body part name     |
| `target`    | String | Filter by target muscle name |

### Example Request

#### Retrieve Exercises by Equipment

```bash
GET /api/v1/exercises/?equipment=dumbbell
```

#### Response

```json
{
  "status": "success",
  "message": "Exercises fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "Dumbbell Bench Press",
      "bodypart": "Chest",
      "equipment": "Dumbbell",
      "target": "Pectorals"
    }
  ]
}
```

---

## Filtering Logic

The API supports filtering exercises using query parameters. The logic is implemented in the `get_queryset` method:

```python
class ExerciseViewset(viewsets.ModelViewSet):
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
            target = Target.objects.filter(name=target_query).first()
            queryset = queryset.filter(target=target)

        return queryset
```

---

## OpenAPI Documentation

### Description

This API is documented using `drf-yasg` to provide an interactive interface.

### Integration of Query Parameters:

The Swagger documentation explicitly includes query parameters for filtering:

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ExerciseViewset(viewsets.ModelViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('equipment', openapi.IN_QUERY, description="Equipment name", type=openapi.TYPE_STRING),
            openapi.Parameter('bodyPart', openapi.IN_QUERY, description="Body Part name", type=openapi.TYPE_STRING),
            openapi.Parameter('target', openapi.IN_QUERY, description="Target muscle group name", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        # List logic
```

### Access Documentation

Swagger documentation is available at:
`http://<server-domain>/api/swagger/`

---

## Caching

Caching is implemented using dynamic cache keys for enhanced performance.

### Cache Key Implementation

```python
from django.core.cache import cache

class ExerciseViewset(viewsets.ModelViewSet):
    def _generate_cache_key(self, prefix, request=None, **kwargs):
        query_string = request.META.get('QUERY_STRING', '')
        hashed_query = hashlib.md5(query_string.encode()).hexdigest()
        return f"{prefix}_{hashed_query}"
```

Cache duration is set to **15 minutes**.

---

## Additional Routers

The following additional endpoints are registered for supplementary data:

```python
router.register('equipment-list', EquipmentViewset, basename='equipment-list')
router.register('body-list', BodyPartViewset, basename='body-list')
router.register('target-list', TargetViewset, basename='target-list')
```

These endpoints provide detailed lists of equipment, body parts, and targets to assist in exercise filtering.

---

## Data and Media Usage

The data and GIF images used in this project are sourced from ExerciseDB and are intended **only for learning purposes**.

---

## Contributing

We welcome contributions! Please follow the steps below:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-branch-name
   ```
5. Create a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---
