from datetime import date
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
 
@csrf_exempt
def get(request):
    if request.method == 'GET':
        # Extract user_id from the request data
        user_id = request.GET.get('user_id')

        if user_id:
            # Get the current date
            current_date = date.today()  # Use date object

            with connection.cursor() as cursor:
                
                cursor.execute("""
                    SELECT e.id, e.title, e.start_date, e.duration
                    FROM exams e
                    LEFT JOIN candidate_exam ce ON e.id = ce.exam_id AND ce.user_id = %s
                    WHERE ce.user_id IS NULL AND e.start_date >= %s
                    """, [user_id, current_date])


                exam_data = cursor.fetchall()

                if exam_data:
                    exams = []
                    for exam_row in exam_data:
                        exam_id, title, start_date, duration = exam_row
                        exams.append({
                            'exam_id': exam_id,
                            'title': title,
                            'start_date': start_date.strftime("%Y-%m-%d"),
                            'duration': duration
                        })

                    return JsonResponse({'exams': exams})
                else:
                    return JsonResponse({'message': 'No  exams for the student'}, status=404)
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
