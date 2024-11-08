# from django.db import connection
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def login_user(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         email = data.get('email')
#         password = data.get('password')

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT * FROM aaas.user WHERE email = %s AND password = %s",
#                 [email, password]
#             )
#             user_data = cursor.fetchone()

#         if user_data:
#             # User found, check role and return success
#             user_id, full_name, email, password, photo, status, role, _ = user_data

#             # Decode byte objects to strings if they are bytes
#             password = password.decode('utf-8') if isinstance(password, bytes) else password
#             photo = photo.decode('utf-8') if isinstance(photo, bytes) else photo

#             return JsonResponse({
#                 'success': 'Login successful',
#                 'user_id': user_id,
#                 'full_name': full_name,
#                 'email': email,
#                 'password': password,
#                 'photo': photo,
#                 'status': status,
#                 'role': role,
#             })
#         else:
#             # User not found or incorrect credentials
#             return JsonResponse({'error': 'Invalid credentials'})

#     return JsonResponse({'error': 'Invalid request method'})

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        email = data.get('email')
        password = data.get('password')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM aaas.user WHERE email = %s AND password = %s",
                [email, password]
            )
            user_data = cursor.fetchone()

        if user_data:
            # User found, check role and return success
            (
                user_id,
                full_name,
                email,
                password,
                photo,
                status,
                role,
                time,
                reference_number,
                field,
                degree,
            ) = user_data

            # Decode byte objects to strings if they are bytes
            password = password.decode('utf-8') if isinstance(password, bytes) else password
            photo = photo.decode('utf-8') if isinstance(photo, bytes) else photo

            return JsonResponse(
                {
                    "success": "Login successful",
                    "user_id": user_id,
                    "full_name": full_name,
                    "email": email,
                    "password": password,
                    "photo": photo,
                    "status": status,
                    "role": role,
                    "time": time,
                    "reference_number": reference_number,
                    "field": field,
                    "degree": degree,
                }
            )
        else:
            # User not found or incorrect credentials
            return JsonResponse({'error': 'Invalid credentials'})

    return JsonResponse({"error": "Invalid request method"})
