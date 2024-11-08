from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_roles(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role_name = data.get('role_name')
        status = data.get('status')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_roles (role_name, status) VALUES (%s, %s)", [role_name, status])
            return JsonResponse({'message': 'Role added successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
