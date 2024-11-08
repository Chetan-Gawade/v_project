from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pending_exams(request):
    if request.method == 'GET':
        # Extract user_id from the request data
        user_id = request.GET.get('user_id')

        if user_id:
            with connection.cursor() as cursor:
                cursor.execute("""
    SELECT ce.exam_id, ce.user_id, u.full_name, e.title
    FROM candidate_exam ce
    INNER JOIN exams e ON ce.exam_id = e.id
    INNER JOIN user u ON ce.user_id = u.user_id
    WHERE ce.approval_status = 'N'
    AND e.creator = %s
""", [user_id])


                rows = cursor.fetchall()

                # Convert the rows into a list of dictionaries
                results = []
                for row in rows:
                    result_dict = {
                        'exam_id': row[0],
                        'user_id': row[1],
                        'full_name': row[2],
                        'title': row[3]
                    }
                    results.append(result_dict)

                return JsonResponse({'status': 'success', 'data': results})
        else:
            return JsonResponse({'status': 'error', 'message': 'User ID not provided'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed.'}, status=405)
