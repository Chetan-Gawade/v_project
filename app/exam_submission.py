
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# @csrf_exempt
# def exam_submission(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         exam_id = data.get('exam_id')
#         user_id = data.get('user_id')
#         question_id = data.get('question_id')
#         option_id = data.get('option_id')
#         option = data.get('option')

#         # Use Django cursor to execute raw SQL query
#         with connection.cursor() as cursor:
#             sql = """
#             INSERT INTO submission (exam_id, user_id, questions_id, option_id, option)
#             VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute(sql, [exam_id, user_id, question_id, option_id, option])

#         return JsonResponse({'message': 'Submission saved successfully'}, status=201)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)





# @csrf_exempt
# def exam_submission(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             if not isinstance(data, dict):
#                 raise ValueError("Invalid JSON format: Expected a dictionary")
            
#             exam_id = data.get('exam_id')
#             user_id = data.get('user_id')
#             question_id = data.get('question_id')
#             option_id = data.get('option_id')
#             option = data.get('option')

#             # Use Django cursor to execute raw SQL query
#             with connection.cursor() as cursor:
#                 sql = """
#                 INSERT INTO submission (exam_id, user_id, questions_id, option_id, option)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(sql, [exam_id, user_id, question_id, option_id, option])

#             return JsonResponse({'message': 'Submission saved successfully'}, status=201)
#         except ValueError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def exam_submission(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            if not isinstance(data, list):
                raise ValueError("Invalid JSON format: Expected a list of dictionaries")

            for submission in data:
                exam_id = submission.get('exam_id')
                user_id = submission.get('user_id')
                question_id = submission.get('question_id')
                option_id = submission.get('option_id')
                option = submission.get('option')

                # Use Django cursor to execute raw SQL query
                with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO submission (exam_id, user_id, questions_id, option_id, option)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, [exam_id, user_id, question_id, option_id, option])

            return JsonResponse({'message': 'Submissions saved successfully'}, status=201)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
