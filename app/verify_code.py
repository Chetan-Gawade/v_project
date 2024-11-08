# import datetime
# import random
# from django.db import connection
# from django.http import JsonResponse
# from django.core.mail import send_mail
# from django.views.decorators.csrf import csrf_exempt
# import json


# @csrf_exempt
# def verify_otp(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         otp_entered = data.get('otp')
 
#         if not user_id or not otp_entered:
#             return JsonResponse({'error': 'User ID and OTP are required'}, status=400)
 
#         # Check if the OTP exists in the database for the given user ID and is still valid (e.g., within 5 minutes)
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT otp_value, created_at FROM otp WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", [user_id])
#             otp_data = cursor.fetchone()
 
#             if not otp_data:
#                 return JsonResponse({'error': 'No OTP found for this user'}, status=404)
 
#             otp_value, created_at = otp_data
 
#             # Check if the OTP matches and is still valid (within 5 minutes)
#             if otp_value == otp_entered and (datetime.datetime.now() - created_at).total_seconds() < 300:
#                 # OTP is valid, proceed with further processing (e.g., password reset)
#                 # Your logic here...
#                 return JsonResponse({'message': 'OTP verification successful'})
#             else:
#                 return JsonResponse({'error': 'Invalid OTP or OTP has expired'}, status=400)
 
#     return JsonResponse({'error': 'Invalid request method'}, status=400)
import json
import logging
from datetime import datetime, timezone
from django.db import connection
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = int(data.get('user_id'))  # Convert user_id to integer
            otp_entered = data.get('otp')

            if not user_id or not otp_entered:
                return JsonResponse({'error': 'User ID and OTP are required'}, status=400)

            # Get the latest OTP entry from the database for the given user ID and OTP value
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT otp_value, created_at FROM otp WHERE user_id = %s AND otp_value = %s ORDER BY created_at DESC LIMIT 1",
                    [user_id, otp_entered]
                )
                otp_data = cursor.fetchone()

            if not otp_data:
                return JsonResponse({'error': 'Invalid OTP or OTP has expired'}, status=400)

            # Extract OTP value and creation timestamp
            otp_value, created_at = otp_data

            # Convert creation timestamp to timezone-aware datetime
            created_at = make_aware(created_at)

            # Get current time in UTC
            current_time_utc = datetime.now(timezone.utc)

            # Calculate time difference between current time and OTP creation time
            time_difference = current_time_utc - created_at

            # Check if the OTP is still valid (within 5 minutes)
            if time_difference.total_seconds() < 300:
                # OTP is valid, proceed with further processing (e.g., password reset)
                # Your logic here...
                return JsonResponse({'message': 'OTP verification successful'})
            else:
                # OTP has expired
                return JsonResponse({'error': 'Invalid OTP or OTP has expired'}, status=400)

        except Exception as e:
            error_msg = "Error occurred while verifying OTP: {}".format(str(e))
            logger.exception(error_msg)
            return JsonResponse({'error': error_msg}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
