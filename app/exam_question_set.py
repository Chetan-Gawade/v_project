# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.db import connection

# @csrf_exempt
# def add_question_to_exam(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             exam_id = data.get('id')  # Corrected variable name to match 'id' in frontend
#             question_ids = data.get('questions_id', [])  # Corrected variable name to match 'questions_id' in frontend
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
#         if not (exam_id and question_ids):
#             return JsonResponse({'error': 'Both exam ID and question IDs are required.'}, status=400)

#         try:
#             with connection.cursor() as cursor:
#                 # Check if the exam exists
#                 cursor.execute("SELECT * FROM exams WHERE id = %s", [exam_id])
#                 exam = cursor.fetchone()
#                 if not exam:
#                     return JsonResponse({'error': 'Exam with the specified ID does not exist.'}, status=404)

#                 # Insert each question ID along with the exam ID into the exam_question_set table
#                 for question_id in question_ids:
#                     cursor.execute("INSERT INTO exam_question_set (id, questions_id) VALUES (%s, %s)", [exam_id, question_id])  # Corrected variable name to match 'exam_id'
                
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
        
#         return JsonResponse({'message': 'Questions added to the exam successfully.', 'id': exam_id, 'questions_id': question_ids})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
#     #14:19







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection

@csrf_exempt
def add_question_to_exam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            exam_id = data.get('id')
            question_ids = data.get('questions_id', [])
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        if not (exam_id and question_ids):
            return JsonResponse({'error': 'Both exam ID and question IDs are required.'}, status=400)

        try:
            with connection.cursor() as cursor:
                # Check if the exam exists
                cursor.execute("SELECT * FROM exams WHERE id = %s", [exam_id])
                exam = cursor.fetchone()
                if not exam:
                    return JsonResponse({'error': 'Exam with the specified ID does not exist.'}, status=404)

                total_marks = 0  # Initialize total marks
                # Iterate through each question ID to calculate total marks
                for question_id in question_ids:
                    cursor.execute("SELECT marks FROM questions WHERE questions_id = %s", [question_id])
                    question_marks = cursor.fetchone()
                    if question_marks:
                        total_marks += question_marks[0]  # Add question marks to total marks
                
                # Update the marks in the exams table
                cursor.execute("UPDATE exams SET marks = %s WHERE id = %s", [total_marks, exam_id])
                
                # Insert each question ID along with the exam ID into the exam_question_set table
                for question_id in question_ids:
                    cursor.execute("INSERT INTO exam_question_set (id, questions_id) VALUES (%s, %s)", [exam_id, question_id])
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        return JsonResponse({'message': 'Questions added to the exam successfully.', 'id': exam_id, 'questions_id': question_ids})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

