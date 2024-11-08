# from django.db import connection
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# # Decorator to exempt CSRF validation for this view
# @csrf_exempt
# def exam_result(request):
#     if request.method == 'POST':
#         try:
#             # Decode the request body and load it as JSON
#             data = json.loads(request.body.decode('utf-8'))

#             # Check if the required keys are present in the data for each question
#             for entry in data:
#                 if 'exam_id' not in entry or 'user_id' not in entry or 'question_id' not in entry or 'option_id' not in entry:
#                     raise ValueError("Invalid data format. Required keys are missing.")

#             # Extract common values like exam_id and user_id assuming they are the same for all entries
#             exam_id = data[0].get('exam_id')
#             user_id = data[0].get('user_id')
#             options_data = data

#             # Save submission
#             with connection.cursor() as cursor:
#                 for option in options_data:
#                     question_id = option.get('question_id')  # Assuming question_id is passed from frontend
#                     selected_options = option.get('option_id')  # Assuming option_id is passed as a list

#                     # Insert each option ID into the database separately
#                     for option_id in selected_options:
#                         cursor.execute("""
#                             INSERT INTO submission (exam_id, user_id, questions_id, option_id)
#                             VALUES (%s, %s, %s, %s)
#                         """, [exam_id, user_id, question_id, option_id])

#             # Calculate result
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT marks FROM exams WHERE id = %s
#                 """, [exam_id])
#                 exam_marks = cursor.fetchone()

#                 if not exam_marks:
#                     return JsonResponse({'status': 'failed', 'message': 'Invalid exam ID'})

#                 total_marks = exam_marks[0]
#                 marks = 0

#                 for option in options_data:
#                     question_id = option.get('question_id')  # Assuming question_id is passed from frontend
#                     selected_options = option.get('option_id')  # Assuming option_id is passed as a list

#                     # Iterate over each selected option ID
#                     for selected_option_id in selected_options:
#                         cursor.execute("""
#                             SELECT is_correct, q.marks
#                             FROM questions_option qo
#                             INNER JOIN questions q ON qo.questions_id = q.questions_id
#                             WHERE qo.questions_id = %s AND qo.option_id = %s
#                         """, [question_id, selected_option_id])
#                         result = cursor.fetchone()

#                         if result and result[0] == 'Y':
#                             marks += result[1]

#                 if total_marks != 0:
#                     percentage = (marks / total_marks) * 100
#                 else:
#                     percentage = 0

#                 cursor.execute("""
#                     INSERT INTO result (exam_id, user_id, marks, percentage, total_marks)
#                     VALUES (%s, %s, %s, %s, %s)
#                     ON DUPLICATE KEY UPDATE marks = %s, percentage = %s, total_marks = %s
#                 """, [exam_id, user_id, marks, percentage, total_marks, marks, percentage, total_marks])

#                 connection.commit()

#                 response_data = {
#                     'status': 'success',
#                     'marks': marks,
#                     'percentage': f"{percentage:.2f}%",
#                     'total_marks': total_marks
#                 }
#                 return JsonResponse(response_data)

#         except Exception as e:
#             return JsonResponse({'status': 'failed', 'message': f"Error: {str(e)} Data: {data}"})

#     else:
#         return JsonResponse({'status': 'failed', 'message': 'Only POST requests are allowed'})


# ffrom django.db import connection
# from django.db import connection  # Import connection from django.db
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def exam_result(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))

#             # Check for required keys in each entry of data
#             for entry in data:
#                 if not all(
#                     key in entry
#                     for key in ("exam_id", "user_id", "question_id", "option_id")
#                 ):
#                     raise ValueError("Invalid data format. Required keys are missing.")

#             exam_id = data[0]["exam_id"]
#             user_id = data[0]["user_id"]

#             # Save submission
#             with connection.cursor() as cursor:
#                 for option in data:
#                     question_id = option["question_id"]
#                     selected_options = option["option_id"]

#                     for option_id in selected_options:
#                         cursor.execute("""
#                             INSERT INTO submission (exam_id, user_id, questions_id, option_id)
#                             VALUES (%s, %s, %s, %s)
#                         """, [exam_id, user_id, question_id, option_id])

#                 cursor.execute("""
#                     SELECT marks FROM exams WHERE id = %s
#                 """, [exam_id])
#                 exam_marks = cursor.fetchone()

#                 if not exam_marks:
#                     return JsonResponse({'status': 'failed', 'message': 'Invalid exam ID'})

#                 total_marks = exam_marks[0]
#                 marks = 0

#                 for option in data:
#                     question_id = option["question_id"]
#                     selected_options = option["option_id"]

#                     for selected_option_id in selected_options:
#                         cursor.execute("""
#                             SELECT is_correct, q.marks
#                             FROM questions_option qo
#                             INNER JOIN questions q ON qo.questions_id = q.questions_id
#                             WHERE qo.questions_id = %s AND qo.option_id = %s
#                         """, [question_id, selected_option_id])
#                         result = cursor.fetchone()

#                         if result and result[0] == 'Y':
#                             marks += result[1]

#                 percentage = (marks / total_marks) * 100 if total_marks != 0 else 0

#                 cursor.execute("""
#                     INSERT INTO result (exam_id, user_id, marks, percentage, total_marks)
#                     VALUES (%s, %s, %s, %s, %s)
#                     ON DUPLICATE KEY UPDATE marks = %s, percentage = %s, total_marks = %s
#                 """, [exam_id, user_id, marks, percentage, total_marks, marks, percentage, total_marks])

#                 connection.commit()

#                 response_data = {
#                     'status': 'success',
#                     'marks': marks,
#                     'percentage': f"{percentage:.2f}%",
#                     'total_marks': total_marks
#                 }

#                 # Update approval_status in candidate_exam if needed
#                 cursor.execute(
#                     """
#                     UPDATE candidate_exam
#                     SET approval_status = 'N'
#                     WHERE user_id = %s AND exam_id = %s
#                 """,
#                     [user_id, exam_id],
#                 )

#                 return JsonResponse(response_data)

#         except Exception as e:
#             return JsonResponse({"status": "failed", "message": f"Error: {str(e)}"})

#     return JsonResponse(
#         {"status": "failed", "message": "Only POST requests are allowed"}
#     )

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def exam_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Check for required keys in each entry of data
            for entry in data:
                if not all(
                    key in entry
                    for key in ("exam_id", "user_id", "question_id", "option_id")
                ):
                    raise ValueError("Invalid data format. Required keys are missing.")

            exam_id = data[0]["exam_id"]
            user_id = data[0]["user_id"]

            # Save submission
            with connection.cursor() as cursor:
                for option in data:
                    question_id = option["question_id"]
                    selected_options = option["option_id"]

                    for option_id in selected_options:
                        cursor.execute("""
                            INSERT INTO submission (exam_id, user_id, questions_id, option_id)
                            VALUES (%s, %s, %s, %s)
                        """, [exam_id, user_id, question_id, option_id])

            return JsonResponse(
                {"status": "success", "message": "Submission successful"}
            )

        except Exception as e:
            return JsonResponse({"status": "failed", "message": f"Error: {str(e)}"})

    return JsonResponse(
        {"status": "failed", "message": "Only POST requests are allowed"}
    )
