from django.http import JsonResponse
from django.db import connection

def student_result_report(request):
    if request.method == 'GET':

        # Write the SQL query to fetch marks, user full name, exam title, and total marks
        query = """
        SELECT result.marks, result.total_marks, user.full_name, result.exam_id, user.field, user.degree
        FROM result
        JOIN user ON result.user_id = user.user_id
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Group results by exam_id
            results_by_exam = {}
            for row in rows:
                exam_id = row[3]
                if exam_id not in results_by_exam:
                    results_by_exam[exam_id] = []
                results_by_exam[exam_id].append(
                    {
                        "marks": row[0],
                        "total_marks": row[1],
                        "full_name": row[2],
                        "field": row[4],
                        "degree": row[5],
                    }
                )

            # Fetch exam title and combine with results
            result_data = []
            for exam_id, results in results_by_exam.items():
                exam_title = fetch_exam_title(exam_id)
                result_data.append({
                    'exam_title': exam_title,
                    'results': results
                })

            # Return the JSON response
            return JsonResponse({'results': result_data})

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def fetch_exam_title(exam_id):
    # Function to fetch the exam title for a given exam_id
    query = """
    SELECT title
    FROM exams
    WHERE id = %s
    """
 
    with connection.cursor() as cursor:
        cursor.execute(query, [exam_id])
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
