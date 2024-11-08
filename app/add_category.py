
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_name = data.get('category_name')
            if category_name:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO category (Category) VALUES (%s)", [category_name])
                        return JsonResponse({'message': 'Category added successfully'}, status=201)
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Category name cannot be empty'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
