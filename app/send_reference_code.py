# import json
# from django.http import JsonResponse
# from django.core.mail import send_mail
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection

# @csrf_exempt
# def send_reference_code(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

#     try:
#         data = json.loads(request.body)
#         email = data.get('email')
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#     if not email:
#         return JsonResponse({'error': 'Email is required'}, status=400)

#     try:
#         validate_email(email)
#     except ValidationError as e:
#         return JsonResponse({'error': 'Invalid email format'}, status=400)

#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT reference_number FROM user WHERE email=%s", [email])
#             user = cursor.fetchone()

#             if user:
#                 reference_code = user[0]
#                 send_email(email, reference_code)
#                 return JsonResponse({'message': 'Reference code sent successfully'}, status=200)
#             else:
#                 return JsonResponse({'error': 'User not found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# def send_email(email, reference_code):
#     subject = 'Your Reference Code'
#     message = f'''
#     Dear User,

#     Thank you for being a part of our platform.

#     We are pleased to inform you that your reference code is: {reference_code}

#     Please keep this code secure as it will be needed for further interactions.

#     If you have any questions or need further assistance, feel free to contact us.

#     Best regards,
#     The DataTech Labs Team
#     '''
#     from_email = 'pr@thedatatechlabs.com'
#     recipient_list = [email]
    
#     try:
#         send_mail(subject, message, from_email, recipient_list)
#     except Exception as e:
#         return JsonResponse({'error': 'Failed to send email'}, status=500)

import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

@csrf_exempt
def send_reference_code(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)

    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT reference_number FROM user WHERE email=%s", [email])
            user = cursor.fetchone()

            if user:
                reference_code = user[0]
                send_email(email, reference_code)
                return JsonResponse({'message': 'Reference code sent successfully'}, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def send_email(email, reference_code):
    subject = 'Your Reference Code'
    message = f'''
Subject: Your Reference Code

Dear User,
Thank you for being part of the AAAS.
thank you being part of the AAAS . this is your unique reference code: {reference_code}.
This reference code is essential for any further interactions with our platform, so please ensure its safekeeping.
Should you have any queries or require assistance, please do not hesitate to reach out to us.
Warm regards,
AAAS Team
    '''
    from_email = 'pr@thedatatechlabs.com'
    recipient_list = [email]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return JsonResponse({'error': 'Failed to send email'}, status=500)
