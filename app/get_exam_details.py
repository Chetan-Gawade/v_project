
# #updated by sejalkamble..98..........0
# from django.db import connection
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
 
# @csrf_exempt
# def get_exam_details(request):
#     if request.method == 'POST':
#         try:
#             # Extract data from the request body
#             data = json.loads(request.body.decode('utf-8'))
#             user_id = data.get('user_id')
#             exam_id = data.get('exam_id')
 
#             # Write the corrected SQL query
#             query = """
#                 SELECT exams.title, exams.start_date, exams.time, exams.duration, exams.rules
#                 FROM exams
#                 INNER JOIN candidate_exam ON exams.id = candidate_exam.exam_id
#                 WHERE candidate_exam.user_id = %s AND candidate_exam.exam_id = %s
#             """
 
#             # Execute the query using Django cursor
#             with connection.cursor() as cursor:
#                 cursor.execute(query, [user_id, exam_id])
#                 results = cursor.fetchall()
 
#             # Format the results
#             exam_details = []
#             for result in results:
#                 rules_list = result[4].split('\n')  # Split rules string into a list using newline characters
#                 exam_details.append({
#                     'title': result[0],
#                     'start_date': result[1],
#                     'time': result[2],
#                     'duration': result[3],
#                     'rules': rules_list,
#                 })
 
#             # Return the JSON response
#             return JsonResponse({'exam_details': exam_details})
 
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
 
#     else:
#         return JsonResponse({'error': 'Invalid request method'})




# # New updated by sejal
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta

@csrf_exempt
def get_exam_details(request):
    if request.method == 'POST':
        try:
            # Extract data from the request body
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            exam_id = data.get('exam_id')

            if not user_id or not exam_id:
                return JsonResponse({'error': 'user_id and exam_id are required'}, status=400)

            # Write the corrected SQL query
            query = """
                SELECT exams.title, exams.start_date, exams.time, exams.duration, exams.rules
                FROM exams
                INNER JOIN candidate_exam ON exams.id = candidate_exam.exam_id
                WHERE candidate_exam.user_id = %s AND candidate_exam.exam_id = %s
            """

            # Execute the query using Django cursor
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id, exam_id])
                results = cursor.fetchall()

            if not results:
                return JsonResponse({'error': 'No exam details found for the given user_id and exam_id'}, status=404)

            # Define fixed extra time
            fixed_extra_time = 20  # 20 minutes

            # Format the results
            exam_details = []
            for result in results:
                title, start_date, time, duration, rules = result
                rules_list = rules.split('\n')  # Split rules string into a list using newline characters

                # Ensure duration is an integer
                duration = int(duration)

                # Calculate total exam duration (start time + fixed extra time)
                start_datetime = datetime.strptime(f"{start_date} {time}", '%Y-%m-%d %H:%M:%S')
                total_duration = timedelta(minutes=duration) + timedelta(minutes=fixed_extra_time)
                end_time = start_datetime + total_duration
                extra_time_str = end_time.strftime('%H:%M:%S')
                
                current_time = datetime.now()
                time_left = max((end_time - current_time).total_seconds(), 0)

                exam_details.append({
                    'title': title,
                    'start_date': start_date,
                    'time': time,
                    'duration': duration,
                    'extra_time': extra_time_str,
                    'rules': rules_list,
                   
                })

            # Return the JSON response
            return JsonResponse({'exam_details': exam_details})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
