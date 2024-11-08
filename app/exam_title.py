# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.db import connection

# @csrf_exempt
# def user_exam_results(request):
#     if request.method == 'POST':
#         try:
#             # Parse the request body to get user_id
#             data = json.loads(request.body)
#             user_id = data['user_id']
#         except (json.JSONDecodeError, KeyError) as e:
#             # Handle JSON decode error or missing key in request body
#             return JsonResponse({'error': 'Invalid or missing user_id in request body'}, status=400)

#         # Fetch exam data for the specified user_id
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT exams.title, result.user_id, result.percentage
#                 FROM result
#                 INNER JOIN exams ON result.exam_id = exams.id
#                 WHERE result.user_id = %s
#                 ORDER BY result.exam_id
#                 LIMIT 10;
#             """, [user_id])

#             rows = cursor.fetchall()

#         # Prepare the response data with additional logic
#         results_data = []
#         for row in rows:
#             exam_title, user_id, percentage = row
#             pass_status = "Pass" if percentage > 50 else "Fail"
#             results_data.append({
#                 "exam_title": exam_title,
#                 "user_id": user_id,
#                 "percentage": percentage,
#                 "pass_status": pass_status
#             })

#         # Return the response as JSON
#         return JsonResponse({'data': results_data})
#     else:
#         # Return error response for non-POST requests
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
















# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.db import connection

# @csrf_exempt
# def user_exam_results(request):
#     if request.method == 'POST':
#         try:
#             # Parse the request body to get user_id
#             data = json.loads(request.body)
#             user_id = data['user_id']
#         except (json.JSONDecodeError, KeyError) as e:
#             # Handle JSON decode error or missing key in request body
#             return JsonResponse({'error': 'Invalid or missing user_id in request body'}, status=400)

#         # Fetch the latest three exam results for the specified user_id
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT exams.title, result.user_id, result.percentage
#                 FROM result
#                 INNER JOIN exams ON result.exam_id = exams.id
#                 WHERE result.user_id = %s
#                 ORDER BY exams.start_date DESC
#                 LIMIT 3;
#             """, [user_id])

#             rows = cursor.fetchall()

#         # Prepare the response data with additional logic
#         results_data = []
#         for row in rows:
#             exam_title, user_id, percentage = row
#             pass_status = "Pass" if percentage > 50 else "Fail"
#             results_data.append({
#                 "exam_title": exam_title,
#                 "user_id": user_id,
#                 "percentage": percentage,
#                 "pass_status": pass_status
#             })

#         # Return the response as JSON
#         return JsonResponse({'data': results_data})
#     else:
#         # Return error response for non-POST requests
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)




#code
# from datetime import date
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def user_exam_results(request):
#     if request.method == 'POST':
#         # Load the JSON request body
#         try:
#             body = json.loads(request.body)
#             user_id = body.get('user_id')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

#         if user_id:
#             # Get the current date
#             current_date = date.today()  # Use date object

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT e.id, e.title, e.start_date, e.duration, e.marks
#                     FROM exams e
#                     INNER JOIN candidate_exam ce ON e.id = ce.exam_id
#                     WHERE ce.user_id = %s AND e.start_date >= %s AND ce.approval_status = 'Y'
#                     ORDER BY e.start_date ASC
#                     LIMIT 2
#                     """, [user_id, current_date])

#                 exam_data = cursor.fetchall()

#                 if exam_data:
#                     exams = []
#                     for exam_row in exam_data:
#                         exam_id, title, start_date, duration, marks = exam_row
#                         exams.append({
#                             'exam_id': exam_id,
#                             'title': title,
#                             'start_date': start_date.strftime("%Y-%m-%d"),
#                             'duration': duration,
#                             'marks': marks
#                         })

#                     return JsonResponse({'exams': exams})
#                 else:
#                     return JsonResponse({'message': 'No upcoming exams for the student'}, status=404)
#         else:
#             return JsonResponse({'error': 'User ID not provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)






#code
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from datetime import date
# from django.db import connection

# @csrf_exempt
# def user_exam_results(request):
#     if request.method == 'POST':
#         # Load the JSON request body to get user_id
#         try:
#             body = json.loads(request.body)
#             user_id = body.get('user_id')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

#         if user_id:
#             # Get the current date
#             current_date = date.today()  # Use date object

#             # Fetch the latest three exam results for the specified user_id
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT exams.title, result.user_id, result.percentage
#                     FROM result
#                     INNER JOIN exams ON result.exam_id = exams.id
#                     WHERE result.user_id = %s
#                     ORDER BY exams.start_date DESC
#                     LIMIT 3;
#                 """, [user_id])

#                 rows = cursor.fetchall()

#                 # Prepare the response data with additional logic
#                 results_data = []
#                 for row in rows:
#                     exam_title, user_id, percentage = row
#                     pass_status = "Pass" if percentage > 50 else "Fail"
#                     results_data.append({
#                         "exam_title": exam_title,
#                         "user_id": user_id,
#                         "percentage": percentage,
#                         "pass_status": pass_status
#                     })

#             # Fetch the next two upcoming exams for the specified user_id
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT e.id, e.title, e.start_date, e.duration, e.marks
#                     FROM exams e
#                     INNER JOIN candidate_exam ce ON e.id = ce.exam_id
#                     WHERE ce.user_id = %s AND e.start_date >= %s AND ce.approval_status = 'Y'
#                     ORDER BY e.start_date ASC
#                     LIMIT 2
#                 """, [user_id, current_date])

#                 exam_data = cursor.fetchall()

#                 # Prepare the response data for upcoming exams
#                 exams = []
#                 for exam_row in exam_data:
#                     exam_id, title, start_date, duration, marks = exam_row
#                     exams.append({
#                         'exam_id': exam_id,
#                         'title': title,
#                         'start_date': start_date.strftime("%Y-%m-%d"),
#                         'duration': duration,
#                         'marks': marks
#                     })

#             # Return the response as JSON with both sets of data
#             return JsonResponse({'latest_exam_results': results_data, 'upcoming_exams': exams})

#         else:
#             return JsonResponse({'error': 'User ID not provided'}, status=400)

#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from django.db import connection

@csrf_exempt
def user_exam_results(request):
    if request.method == 'POST':
        # Load the JSON request body to get user_id
        try:
            body = json.loads(request.body)
            user_id = body.get('user_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

        if user_id:
            # Get the current date
            current_date = date.today()  # Use date object

            # Fetch the latest three exam results for the specified user_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT exams.title, result.user_id, result.percentage
                    FROM result
                    INNER JOIN exams ON result.exam_id = exams.id
                    WHERE result.user_id = %s
                    ORDER BY exams.start_date DESC
                    LIMIT 3;
                """, [user_id])

                rows = cursor.fetchall()

                # Prepare the response data with additional logic
                results_data = []
                for row in rows:
                    exam_title, user_id, percentage = row
                    pass_status = "Pass" if percentage > 50 else "Fail"
                    results_data.append({
                        "exam_title": exam_title,
                        "user_id": user_id,
                        "percentage": percentage,
                        "pass_status": pass_status
                    })

            # Fetch the next two upcoming exams for the specified user_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT e.id, e.title, e.start_date, e.duration, e.marks
                    FROM exams e
                    INNER JOIN candidate_exam ce ON e.id = ce.exam_id
                    WHERE ce.user_id = %s AND e.start_date >= %s AND ce.approval_status = 'Y'
                    ORDER BY e.start_date ASC
                    LIMIT 2
                """, [user_id, current_date])

                exam_data = cursor.fetchall()

                # Prepare the response data for upcoming exams
                exams = []
                for exam_row in exam_data:
                    exam_id, title, start_date, duration, marks = exam_row
                    exams.append({
                        'exam_id': exam_id,
                        'title': title,
                        'start_date': start_date.strftime("%Y-%m-%d"),
                        'duration': duration,
                        'marks': marks
                    })

            # Combine both sets of data into a single dictionary
            response_data = {'latest_exam_results': results_data, 'upcoming_exams': exams}

            # Return the response as JSON with the combined data
            return JsonResponse({'data': response_data})

        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)





