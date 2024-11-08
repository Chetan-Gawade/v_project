
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
 
@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        # Get data from request
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        email = data.get('email')
        feedback = data.get('feedback')
        submission_rating = data.get('submission_rating')
 
        # Check if all required fields are present and not empty
        if user_id is not None and email and feedback and submission_rating is not None:
            with connection.cursor() as cursor:
                # Insert data into database
                sql = "INSERT INTO feedback_submission (user_id, email, feedback, submission_rating) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, email, feedback, submission_rating))
                # Commit the transaction
                connection.commit()
            return JsonResponse({'message': 'Feedback saved successfully'})
        else:
            return JsonResponse({'error': 'Missing required fields or fields are empty'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
 