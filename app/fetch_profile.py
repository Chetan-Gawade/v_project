
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def fetch_profile(request):
#     if request.method == 'GET':
#         # Check user_id in query parameters
#         user_id = request.GET.get('user_id')

#         # If user_id not found in query parameters, check in the request body for JSON data
#         if not user_id:
#             try:
#                 body_data = json.loads(request.body.decode('utf-8'))
#                 user_id = body_data.get('user_id')
#             except json.JSONDecodeError:
#                 pass

#         if not user_id:
#             return JsonResponse({'error': 'user_id is required'}, status=400)

#         # Fetch data from the database using Django's cursor
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute("SELECT meta_value FROM user_meta WHERE user_id = %s", [user_id])
#                 row = cursor.fetchone()
#                 if row:
#                     profile_data = json.loads(row[0])
#                     return JsonResponse(profile_data, status=200)
#                 else:
#                     return JsonResponse({'error': 'Profile not found for the specified user_id'}, status=404)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)








# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json
 
# @csrf_exempt
# def fetch_profile(request):
#     if request.method == 'GET':
#         # Get user_id from the query parameters
#         user_id = request.GET.get('user_id')
 
#         # Check if user_id is provided in the query parameters
#         if not user_id:
#             return JsonResponse({'error': 'user_id is required'}, status=400)
 
#         # Fetch data from the database using Django's cursor
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute("SELECT meta_value FROM user_meta WHERE user_id = %s", [user_id])
#                 row = cursor.fetchone()
#                 if row:
#                     profile_data = json.loads(row[0])
 
#                     # Format the response in the desired structure
#                     response_data = {
#                         "bio": profile_data.get("bio", ""),
#                         "skills": profile_data.get("skills", ""),
#                         "education": profile_data.get("education", ""),
#                         "experience": profile_data.get("experience", "")
#                     }
 
#                     return JsonResponse(response_data, status=200)
#                 else:
#                     return JsonResponse({'error': 'Profile not found for the specified user_id'}, status=404)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
 
#     return JsonResponse({'error': 'Method not allowed'}, status=405)







from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
 
@csrf_exempt
def fetch_profile(request):
    if request.method == 'GET':
        # Get user_id from the query parameters
        user_id = request.GET.get('user_id')
 
        # Check if user_id is provided in the query parameters
        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
 
        # Fetch data from the database using Django's cursor
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT bio, skills, education, experience FROM user_meta WHERE user_id = %s", [user_id])
                row = cursor.fetchone()
                if row:
                    bio, skills, education, experience = row
 
                    # Format the response in the desired structure
                    response_data = {
                        "bio": bio,
                        "skills": skills,
                        "education": education,
                        "experience": experience
                    }
 
                    return JsonResponse(response_data, status=200)
                else:
                    return JsonResponse({'error': 'Profile not found for the specified user_id'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'error': 'Method not allowed'}, status=405)
 