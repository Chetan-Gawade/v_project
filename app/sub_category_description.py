from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def fetch(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sub_category_Id = data.get('sub_category_Id', None)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
        if sub_category_Id is None:
            return JsonResponse({'error': 'Sub-category ID not provided'}, status=400)
        
        # Fetch all questions for the given sub_category_id
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT questions_id, description, marks
                FROM questions
                WHERE sub_category_Id = %s
            """, [sub_category_Id])

            question_data = cursor.fetchall()

        # Extract descriptions and marks from fetched data
        questions = [{'questions_id': q[0], 'description': q[1], 'marks': q[2]} for q in question_data]
        
        response_data = {
            'questions': questions
        }

        return JsonResponse(response_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)






# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def fetch(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             sub_category_Id = data.get('sub_category_Id', None)  # Use the same parameter name
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
#         if sub_category_Id is None:
#             return JsonResponse({'error': 'Sub-category ID not provided'}, status=400)
        
#         # Fetch all questions for the given sub_category_id
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT  questions_id, description
#                 FROM questions
#                 WHERE sub_category_Id = %s
#             """, [sub_category_Id])  # Use the same parameter name

#             question_data = cursor.fetchall()  # Fetch all rows

#         # Extract descriptions from fetched data
#         role_data = [{'questions_id': questions[0], 'description': questions[1]} for questions in question_data]
        
#         # return JsonResponse({'descriptions': descriptions, 'questions_id':questions_id})
#         response_data = {
#             'questions': role_data
#         }

#         return JsonResponse(response_data, safe=False)

#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
