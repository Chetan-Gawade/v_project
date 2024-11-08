
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, IntegrityError
import json
 
@csrf_exempt
def delete_exam(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        exam_id = data.get('exam_id')
        if exam_id is None:
            return HttpResponse("Exam ID is required in the request body.", status=400)
        
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    DELETE FROM candidate_exam WHERE exam_id = %s
                """, [exam_id])
            
                cursor.execute("""
                    DELETE FROM exams WHERE id = %s
                """, [exam_id])

                cursor.execute("""
                    DELETE FROM exam_question_set WHERE id= %s
                """, [exam_id])
                
                connection.commit()

                response_data = {'status': 'Exam and associated records deleted successfully'}
                return JsonResponse(response_data)

            except IntegrityError as e:
                return HttpResponse("Integrity Error: {}".format(str(e)), status=400)
            except Exception as e:
                return HttpResponse("An error occurred: {}".format(str(e)), status=500)

    return HttpResponse(status=405)
