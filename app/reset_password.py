from django.db import connection

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import json
 
@csrf_exempt

def reset_password(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body.decode('utf-8'))  # Parse JSON data

            user_id = data.get('user_id')

            new_password = data.get('new_password')
 
            # Validate user_id and new_password

            if not user_id or not new_password:

                return JsonResponse({'message': 'user_id and new_password are required'}, status=400)
 
            # Update password in the database

            with connection.cursor() as cursor:

                cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", [new_password, user_id])
 
            return JsonResponse({'message': 'Password reset successfully'}, status=200)
 
        except Exception as e:

            return JsonResponse({'message': str(e)}, status=500)
 
    elif request.method == 'OPTIONS':

        # Handle preflight OPTIONS request

        response = JsonResponse({'message': 'Preflight request accepted'})

        response['Access-Control-Allow-Origin'] = '*'  # Adjust the origin accordingly

        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'

        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'

        return response
 
    else:

        return JsonResponse({'message': 'Method not allowed'}, status=405)
