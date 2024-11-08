from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def fetch_question_list(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT questions_id, description, marks
                    FROM questions
                """)
                question_data = cursor.fetchall()  # Fetch all rows

            # Extract descriptions and marks from fetched data
            questions = [{'id': row[0], 'description': row[1], 'marks': row[2]} for row in question_data]
            
            return JsonResponse({'questions': questions})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




