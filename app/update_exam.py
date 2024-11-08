
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, IntegrityError
import json

@csrf_exempt
def update_exam(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        with connection.cursor() as cursor:
            try:
                id =data.get('id')
                title = data.get('title')
                start_date = data.get('start_date')
                description = data.get('description')
                time = data.get('time')
                duration = data.get('duration')
                marks = data.get('marks')
                rules = data.get('rules')

                cursor.execute("""
                    UPDATE exams
                    SET title=%s, start_date=%s, description=%s, time=%s, duration=%s, marks=%s, rules=%s
                    WHERE id=%s
                """, [title, start_date, description, time, duration, marks, rules, id])

                connection.commit()

                response_data = {'status': 'Exam updated successfully'}
                return JsonResponse(response_data, status=200)

            except IntegrityError as e:
                return HttpResponse("Integrity Error: {}".format(str(e)), status=400)
            except Exception as e:
                return HttpResponse("An error occurred: {}".format(str(e)), status=500)

    return HttpResponse(status=405)
#madhura
#madhu
