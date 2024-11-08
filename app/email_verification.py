import datetime
import random
from django.db import connection
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
 
@csrf_exempt
def email_verification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
 
        # Validate email
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
 
        # Check if the email exists in your database
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, full_name FROM user WHERE email = %s", [email])
            user = cursor.fetchone()
 
            if not user:
                return JsonResponse({'error': 'User with this email does not exist'}, status=404)
 
            user_id = user[0]
            user_name = user[1]
 
            # Generate a unique 6-digit OTP 
            max_attempts = 10
            for _ in range(max_attempts):
                otp = random.randint(100000, 999999)
 
                # Check if OTP already exists in the OTP table
                cursor.execute("SELECT COUNT(*) FROM otp WHERE otp_value = %s", [otp])
                count = cursor.fetchone()[0]
 
                if count == 0:
                    # OTP is unique, store it in the OTP table
                    cursor.execute("INSERT INTO otp (user_id, otp_value, created_at) VALUES (%s, %s, %s)",
                                   [user_id, otp, datetime.datetime.now()])
                    break
 
            else:
                # Failed to generate a unique OTP after max_attempts
                return JsonResponse({'error': 'Unable to generate a unique OTP. Please try again.'}, status=500)
 
            # Send reset link to user's email
            subject = 'Password Reset OTP'
            message = f'''
Subject: Password Reset OTP
Dear {user_name},
You have requested to reset your password. Please use the following One-Time Password (OTP) to verify your identity and reset your password:
OTP: {otp}
Note: Do not share this OTP with anyone.
If you did not request this password reset, please ignore this email.
Thank you,
                        '''
 
            from_email = "pr@thedatatechlabs.com"  
            to_email = [email]
  
            try:
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                response_data = {
                    'message': 'Password reset OTP sent to your email',
                    'user_id': user_id
                }
                return JsonResponse(response_data)
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'error': 'Error sending email'}, status=500)
 
    return JsonResponse({'error': 'Invalid request method'}, status=400)
 