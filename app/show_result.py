#Madhura
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# import json
 
# @csrf_exempt
# def show_result(request):
#     # Check if the request method is POST
#     if request.method != 'POST':
#         return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
 
#     try:
#         # Load request body as JSON
#         data = json.loads(request.body)
       
#         # Get the user ID from the request body
#         user_id = data.get('user_id')
 
#         # Check if user ID is provided and it's a valid integer
#         if user_id is None:
#             return JsonResponse({"error": "User ID is required"}, status=400)
#         if not isinstance(user_id, int):
#             return JsonResponse({"error": "Invalid user ID"}, status=400)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON format in request body"}, status=400)
 
#     # Define your SQL query to fetch exam titles and results for a specific user
#     query = """
#     SELECT exams.title, result.total_marks, result.marks, result.percentage
#     FROM exams
#     JOIN result ON exams.id = result.exam_id
#     WHERE result.user_id = %s
#     """
 
#     # Execute the query using Django's cursor with proper parameterization
#     with connection.cursor() as cursor:
#         cursor.execute(query, [user_id])
#         rows = cursor.fetchall()
 
#     # Prepare the response data
#     results_data = []
#     for row in rows:
#         exam_title, total_marks, marks, percentage = row
#         pass_status = "Pass" if marks > 50 else "Fail"
#         results_data.append({
#             "exam_title": exam_title,
#             "total_marks": total_marks,
#             "marks_obtained": marks,
#             "percentage": percentage,
#             "pass_status": pass_status
#         })
 
#     # Return the response as JSON
#     return JsonResponse({"results": results_data})



from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def show_result(request):
    # Check if the request method is POST
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        # Load request body as JSON
        data = json.loads(request.body)
       
        # Get the user ID from the request body
        user_id = data.get('user_id')

        # Check if user ID is provided
        if user_id is None:
            return JsonResponse({"error": "User ID is required"}, status=400)

        # Try parsing user_id to integer
        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "Invalid user ID, it must be an integer"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body"}, status=400)

    # Define your SQL query to fetch exam titles and results for a specific user
    query = """
    SELECT exams.title, result.total_marks, result.marks, result.percentage
    FROM exams
    JOIN result ON exams.id = result.exam_id
    WHERE result.user_id = %s
    """

    # Execute the query using Django's cursor with proper parameterization
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        rows = cursor.fetchall()

    # Prepare the response data
    results_data = []
    for row in rows:
        exam_title, total_marks, marks, percentage = row
        pass_status = "Pass" if marks > 50 else "Fail"
        results_data.append({
            "exam_title": exam_title,
            "total_marks": total_marks,
            "marks_obtained": marks,
            "percentage": percentage,
            "pass_status": pass_status
        })

    # Return the response as JSON
    return JsonResponse({"results": results_data})
