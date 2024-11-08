import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def approve_exam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            exams_data = data  # Assuming the whole request body is the list of exams data
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        if not isinstance(exams_data, list):
            return JsonResponse({'status': 'error', 'message': 'Exams data should be a list'}, status=400)

        with connection.cursor() as cursor:
            try:
                for exam_data in exams_data:
                    exam_id = exam_data.get('exam_id')
                    user_id = exam_data.get('user_id')

                    if exam_id is not None and user_id is not None:
                        cursor.execute("""
                            UPDATE candidate_exam 
                            SET approval_status = 'Y' 
                            WHERE exam_id = %s AND user_id = %s
                        """, [exam_id, user_id])
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Exam ID and User ID are required'}, status=400)

                connection.commit()
                return JsonResponse({'status': 'success', 'message': 'Approval status changed successfully'})
            except Exception as e:
                connection.rollback()
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    elif request.method == 'GET':
        # Handle GET request here if needed
        return JsonResponse({'status': 'success', 'message': 'GET request received'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST and GET requests are allowed.'}, status=405)














 #updated
# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def approve_exam(request):
#     if request.method == 'POST':
#         # Extract exam_id and user_id from the request data
#         try:
#             data = json.loads(request.body)
#             exams = data.get('exams')
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

#         if exams:
#             with connection.cursor() as cursor:
#                 try:
#                     for exam in exams:
#                         exam_id = exam.get('exam_id')
#                         user_id = exam.get('user_id')

#                         if exam_id is not None and user_id is not None:
#                             # Update approval_status to 'Y' for the given exam_id and user_id
#                             cursor.execute("""
#                                 UPDATE candidate_exam 
#                                 SET approval_status = 'Y' 
#                                 WHERE exam_id = %s AND user_id = %s
#                             """, [exam_id, user_id])

#                     # Commit the transaction
#                     connection.commit()

#                     return JsonResponse({'status': 'success', 'message': 'approval status changed successfully'})
#                 except Exception as e:
#                     # Rollback the transaction in case of error
#                     connection.rollback()
#                     return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Exam ID and User ID are required'}, status=400)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)



# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def approve_exam(request):
#     if request.method == 'POST':
#         # POST request logic to update approval status
#         try:
#             data = json.loads(request.body)
#             exam_id = data.get('exam_id')
#             user_id = data.get('user_id')
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

#         if exam_id is not None and user_id is not None:
#             with connection.cursor() as cursor:
#                 try:
#                     cursor.execute("""
#                         UPDATE candidate_exam 
#                         SET approval_status = 'Y' 
#                         WHERE exam_id = %s AND user_id = %s
#                     """, [exam_id, user_id])
#                     connection.commit()
#                     return JsonResponse({'status': 'changed to Y', 'message': 'approval status change successfully'})
#                 except Exception as e:
#                     connection.rollback()
#                     return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Exam ID and User ID are required'}, status=400)
#     elif request.method == 'GET':
#         # GET request logic to retrieve approval status
#         exam_id = request.GET.get('exam_id')
#         user_id = request.GET.get('user_id')

#         if exam_id is not None and user_id is not None:
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT approval_status 
#                     FROM candidate_exam 
#                     WHERE exam_id = %s AND user_id = %s
#                 """, [exam_id, user_id])
#                 row = cursor.fetchone()
#                 if row:
#                     approval_status = row[0]
#                     return JsonResponse({'status': 'success', 'approval_status': approval_status})
#                 else:
#                     return JsonResponse({'status': 'error', 'message': 'Record not found'}, status=404)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Exam ID and User ID are required'}, status=400)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Only POST and GET requests are allowed.'}, status=405)
