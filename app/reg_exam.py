from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def exams(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            exam_id = data.get('exam_id')
            user_id = data.get('user_id')

            if exam_id and user_id:
                # Execute raw SQL query using cursor
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO candidate_exam (exam_id, user_id, approval_status) VALUES (%s, %s, 'N')",
                        [exam_id, user_id]
                    )

                # Return success response
                return JsonResponse({'status': 'success', 'message': 'Candidate registered successfully.'})
            else:
                # Return error response if exam_id or user_id is missing
                return JsonResponse({'status': 'error', 'message': 'exam_id and user_id are required.'}, status=400)
        except json.JSONDecodeError:
            # Return error response if request body is not valid JSON
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    else:
        # Return error response for non-POST requests
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)
