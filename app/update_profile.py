
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def update_profile(request):
#     if request.method == 'PUT':
#         # Extract data from PUT request
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'user_id is required'}, status=400)

#         bio = data.get('bio')
#         skills = data.get('skills')
#         education = data.get('education')
#         experience = data.get('experience')

#         # Check if the user_id exists in the database
#         user_exists = False
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT COUNT(*) FROM user_meta WHERE user_id = %s", [user_id])
#             row = cursor.fetchone()
#             if row[0] > 0:
#                 user_exists = True

#         if not user_exists:
#             return JsonResponse({'error': 'User profile does not exist'}, status=404)

#         # Convert data to JSON format
#         profile_data = {
#             'bio': bio,
#             'skills': skills,
#             'education': education,
#             'experience': experience
#         }

#         # Update data in the database using Django's cursor
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute("UPDATE user_meta SET meta_value = %s WHERE user_id = %s", [json.dumps(profile_data), user_id])
#                 return JsonResponse({'message': 'Profile updated successfully'}, status=200)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)




from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
 
@csrf_exempt
def update_profile(request):
    if request.method == 'PUT':
        # Extract data from PUT request
        data = json.loads(request.body)
        print("Received data:", data)  # Debug print
 
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
 
        # Extract fields that can be updated
        bio = data.get('bio')
        skills = data.get('skills')
        education = data.get('education')
        experience = data.get('experience')
 
        # Check if the user_id exists in the database
        user_exists = False
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user_meta WHERE user_id = %s", [user_id])
            row = cursor.fetchone()
            if row[0] > 0:
                user_exists = True
 
        if not user_exists:
            return JsonResponse({'error': 'User profile does not exist'}, status=404)
 
        # Update data in the database using Django's cursor
        with connection.cursor() as cursor:
            try:
                # Update only the fields that can be modified
                sql_query = "UPDATE user_meta SET bio = %s, skills = %s, education = %s, experience = %s WHERE user_id = %s"
                print("Executing SQL query:", sql_query % (bio, skills, education, experience, user_id))  # Debug print
                cursor.execute(sql_query, [bio, skills, education, experience, user_id])
                return JsonResponse({'message': 'Profile updated successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
 
    return JsonResponse({'error': 'Method not allowed'}, status=405)
 
