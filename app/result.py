# from django.db import connection
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# import json

# @csrf_exempt
# @require_POST
# def result(request):
#     try:
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         exam_id = data.get('exam_id')

#         if user_id is None or exam_id is None:
#             return JsonResponse({'error': 'user_id and exam_id are required fields.'}, status=400)

#         # Execute raw SQL query using cursor
#         with connection.cursor() as cursor:
#             query = """
#                 SELECT total_marks, marks, percentage
#                 FROM result
#                 WHERE user_id = %s AND exam_id = %s
#             """
#             cursor.execute(query, [user_id, exam_id])
#             result = cursor.fetchone()

#         if result:
#             response_data = {
#                 'total_marks': result[0],
#                 'marks': result[1],
#                 'percentage': float(result[2]),  # Ensure percentage is converted to float
#             }
#             return JsonResponse(response_data)
#         else:
#             return JsonResponse({'error': 'Result not found for the given user_id and exam_id.'}, status=404)

#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON data.'}, status=400)


from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def result(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        exam_id = data.get('exam_id')

        if user_id is None or exam_id is None:
            return JsonResponse({'error': 'user_id and exam_id are required fields.'}, status=400)

        with connection.cursor() as cursor:
            # Query to fetch exam result
            result_query = """
                SELECT COUNT(*) FROM aaas.questions_option qo 
                INNER JOIN aaas.submission s ON qo.option_id = s.option_id
                WHERE s.exam_id = %s AND s.user_id = %s AND is_correct = 'Y'; 
            """
            cursor.execute(result_query, [exam_id, user_id])
            marks = cursor.fetchone()[0]

            marks_query = """
                SELECT start_date, marks FROM aaas.exams
                WHERE id = %s;
            """

            cursor.execute(marks_query, [exam_id])
            start_date, total_marks = cursor.fetchone()

            percentage = 0.0

            # print(marks, total_marks)

            if total_marks != 0:
                percentage = (marks / total_marks) * 100

            cursor.execute(
                """
                INSERT INTO result (exam_id, user_id, marks, percentage, total_marks)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE marks = %s, percentage = %s, total_marks = %s
            """,
                [
                    exam_id,
                    user_id,
                    marks,
                    percentage,
                    total_marks,
                    marks,
                    percentage,
                    total_marks,
                ],
            )

            connection.commit()

            exam_delete_query = """
                DELETE FROM aaas.candidate_exam WHERE (exam_id = %s AND user_id = %s);
            """

            cursor.execute(exam_delete_query, [exam_id, user_id])

            connection.commit()

            # Query to fetch user degree and field
            degree_query = """
                SELECT degree, field
                FROM user
                WHERE user_id = %s
            """
            cursor.execute(degree_query, [user_id])
            degree = cursor.fetchone()

        if result and degree:
            response_data = {
                "total_marks": total_marks,
                "marks": marks,
                "percentage": round(
                    percentage, 2
                ),  # Ensure percentage is converted to float
                "degree": degree[0],  # Add degree to the response
                "field": degree[1],  # Add field to the response
                "result_date": start_date,
            }
            return JsonResponse(response_data)
        elif result:
            return JsonResponse(
                {"error": "Degree and field not found for the given user_id."},
                status=404,
            )
        else:
            return JsonResponse({'error': 'Result not found for the given user_id and exam_id.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
