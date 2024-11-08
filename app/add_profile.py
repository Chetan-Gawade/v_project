
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json
 
# @csrf_exempt
# def add_profile(request):
#     if request.method == 'POST':
#         # Extract data from POST request
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'user_id is required'}, status=400)
 
#         # Retrieve user role from the database
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT role FROM user WHERE user_id = %s", [user_id])
#             user_role = cursor.fetchone()
 
#         if not user_role:
#             return JsonResponse({'error': 'User not found'}, status=404)
 
#         # Check if the user's role is 3 (assuming 'role' is the column name in the 'user' table)
#         if user_role[0] != 3:
#             return JsonResponse({'error': 'user id is invalid'}, status=403)
 
#         bio = data.get('bio')
#         skills = data.get('skills')
#         education = data.get('education')
#         experience = data.get('experience')
 
#         # Convert data to JSON format
#         profile_data = {
#             'bio': bio,
#             'skills': skills,
#             'education': education,
#             'experience': experience
#         }
 
#         # Insert data into the database using Django's cursor
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute("INSERT INTO user_meta(user_id, meta_value) VALUES (%s, %s)", [user_id, json.dumps(profile_data)])
#                 return JsonResponse({'message': 'Profile added successfully'}, status=201)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
 
#     return JsonResponse({'error': 'Method not allowed'}, status=405)
 
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def add_profile(request):
#     if request.method == 'POST':
#         # Extract data from POST request
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'user_id is required'}, status=400)

#         # Retrieve user role from the database
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT role FROM user WHERE user_id = %s", [user_id])
#             user_role = cursor.fetchone()

#         if not user_role:
#             return JsonResponse({'error': 'User not found'}, status=404)

#         # Check if the user's role is 3 (assuming 'role' is the column name in the 'user' table)
#         if user_role[0] != 3:
#             return JsonResponse({'error': 'user id is invalid'}, status=403)

#         bio = data.get('bio')
#         skills = data.get('skills')
#         education = data.get('education')
#         experience = data.get('experience')

#         # Convert data to JSON format
#         profile_data = {
#             'bio': bio,
#             'skills': skills,
#             'education': education,
#             'experience': experience
#         }

#         # Insert data into the database using Django's cursor
#         with connection.cursor() as cursor:
#             try:
#                 # If meta_value is not provided, insert NULL
#                 if profile_data:
#                     cursor.execute("INSERT INTO user_meta(user_id, meta_value) VALUES (%s, %s)", [user_id, json.dumps(profile_data)])
#                 else:
#                     cursor.execute("INSERT INTO user_meta(user_id) VALUES (%s)", [user_id])
#                 return JsonResponse({'message': 'Profile added successfully'}, status=201)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)



from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
 
@csrf_exempt
def add_profile(request):
    if request.method == 'POST':
        # Extract data from POST request
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
 
        # Retrieve user role from the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT role FROM user WHERE user_id = %s", [user_id])
            user_role = cursor.fetchone()
 
        if not user_role:
            return JsonResponse({'error': 'User not found'}, status=404)
 
        # Check if the user's role is 3 (assuming 'role' is the column name in the 'user' table)
        if user_role[0] != 3:
            return JsonResponse({'error': 'user id is invalid'}, status=403)
 
        bio = data.get('bio')
        skills = data.get('skills')
        education = data.get('education')
        experience = data.get('experience')
 
        # Insert data into the database using Django's cursor
        with connection.cursor() as cursor:
            try:
                # Execute SQL INSERT statement
                cursor.execute("INSERT INTO user_meta (user_id, bio, skills, education, experience) VALUES (%s, %s, %s, %s, %s)",
                               [user_id, bio, skills, education, experience])
                return JsonResponse({'message': 'Profile added successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'error': 'Method not allowed'}, status=405)