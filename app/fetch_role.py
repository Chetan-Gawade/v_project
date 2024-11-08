from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def fetch_role(request):
    if request.method == 'GET':
        # Fetching role_name and role_id from user_roles
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT role_id, role_name
                FROM user_roles
            """)
            roles = cursor.fetchall()

        # Extracting role names and IDs from the fetched data
        role_data = [{'role_id': role[0], 'role_name': role[1]} for role in roles]

        # Constructing the response dictionary
        response_data = {
            'roles': role_data
        }

        return JsonResponse(response_data, safe=False)
