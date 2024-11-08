
import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
 
@csrf_exempt
def fetch_schedule_exam_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
        with connection.cursor() as cursor:
            # Fetch data from the 'exams' table and join with 'user' table to get creator information
            cursor.execute("""
                SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator
                FROM exams e
                INNER JOIN user u ON e.creator = u.user_id
            """)
            exam_data = cursor.fetchall()  # Fetch all rows
 
            if exam_data:
                exam_list = []
                for exam_row in exam_data:
                    exam_id, title, start_date, marks, duration, creator = exam_row
 
                    exam_info = {
                        'exam_id': exam_id,
                        'title': title,
                        'start_date': start_date.strftime("%Y-%m-%d"),
                        'marks': marks,
                        'duration': duration,
                        'creator': creator,
                    }
                    exam_list.append(exam_info)
 
                return JsonResponse({'exams': exam_list})
            else:
                return JsonResponse({'error': 'No data found in the exams table'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
# import json



