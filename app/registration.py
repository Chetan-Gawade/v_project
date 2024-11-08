
# import random
# import json
# import re
# from django.db import connection, IntegrityError
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import send_mail

# @csrf_exempt
# def register_user(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))

#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')

#         # Password validation
#         password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z]).{8,}$')
#         if not password_pattern.match(password):
#             return JsonResponse({'error': 'Password must be at least 8 characters long, with at least one uppercase letter and one lowercase letter.'})

#         if role not in ['student', 'instructor', 'admin']:
#             return JsonResponse({'error': 'Invalid role. Please choose one of the following roles: student, instructor, admin.'})

#         profile_photo = data.get('profile_photo', '')  # Default to empty string if not provided

#         with connection.cursor() as cursor:
#             try:
#                 # Check if email already exists in the database
#                 cursor.execute("SELECT COUNT(*) FROM aaas.user WHERE email = %s", [email])
#                 if cursor.fetchone()[0] > 0:
#                     return JsonResponse({'error': 'The email address is already registered. Please use a different email address.'})

#                 if role == 'student':
#                     instructor_reference = data.get('instructor_reference')
#                     if instructor_reference == '':
#                         instructor_reference = '1234'  # Default value for instructor reference
#                     elif instructor_reference:
#                         # Check if the instructor reference number exists in the database and corresponds to an instructor
#                         cursor.execute("SELECT COUNT(*) FROM aaas.user WHERE reference_number = %s AND role = 2", [instructor_reference])
#                         if cursor.fetchone()[0] == 0:
#                             instructor_reference = '1234'  # Set to default if invalid
#                     else:
#                         return JsonResponse({'error': 'Please provide the instructor reference number.'})

#                     cursor.execute(
#                         "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
#                         [name, email, password, profile_photo, 'Y', 3, instructor_reference]
#                     )
#                 elif role == 'instructor':
#                     confirm_password = data.get('password')
#                     if confirm_password != password:
#                         return JsonResponse({'error': 'Password and confirm password do not match.'})

#                     reference_number = ''.join(random.choices('0123456789', k=6))  # Generate reference number for instructor

#                     cursor.execute(
#                         "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
#                         [name, email, password, profile_photo, 'Y', 2, reference_number]
#                     )
#                 elif role == 'admin':
#                     confirm_password = data.get('password')
#                     if confirm_password != password:
#                         return JsonResponse({'error': 'Password and confirm password do not match.'})

#                     reference_number = ''.join(random.choices('0123456789', k=6))  # Generate reference number for admin

#                     cursor.execute(
#                         "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
#                         [name, email, password, profile_photo, 'Y', 1, reference_number]
#                     )

#                     # Send email with reference number to the new admin
#                     send_mail(
#                         'Your Admin Reference Number',
#                         f'Hello {name},\n\nYour admin reference number is: {reference_number}\n\nBest regards,\nThe Data Tech Labs Team',
#                         'pr@thedatatechlabs.com',  # Replace with your email address
#                         [email],
#                         fail_silently=False,
#                     )

#                 # Get the auto-generated user_id
#                 user_id = cursor.lastrowid

#                 # Insert user_id into user_meta table where role is 3 (for students)
#                 if role == 'student':
#                     cursor.execute(
#                         "INSERT INTO aaas.user_meta (user_id) VALUES (%s)",
#                         [user_id]
#                     )

#                 return JsonResponse({'success': 'User registered successfully.'})
#             except IntegrityError as e:
#                 return JsonResponse({'error': 'An error occurred during registration. Please try again later.'})

#     return JsonResponse({'error': 'Invalid request method. Please use POST method for registration.'})
import random
import json
import re
from django.db import connection, IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Password validation
        password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z]).{8,}$')
        if not password_pattern.match(password):
            return JsonResponse({'error': 'Password must be at least 8 characters long, with at least one uppercase letter and one lowercase letter.'})

        if role not in ['student', 'instructor', 'admin']:
            return JsonResponse({'error': 'Invalid role. Please choose one of the following roles: student, instructor, admin.'})

        profile_photo = data.get('profile_photo', '')  # Default to empty string if not provided

        with connection.cursor() as cursor:
            try:
                # Check if email already exists in the database
                cursor.execute("SELECT COUNT(*) FROM aaas.user WHERE email = %s", [email])
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({'error': 'The email address is already registered. Please use a different email address.'})

                if role == 'student':
                    instructor_reference = data.get('instructor_reference')
                    field = data.get('field', '')  # Get the field value for the student
                    degree = data.get('degree', '')  # Get the degree value for the student
                    if not field:
                        return JsonResponse({'error': 'Please provide the field of study.'})
                    if not degree:
                        return JsonResponse({'error': 'Please provide the degree.'})
                    if instructor_reference == '':
                        instructor_reference = '1234'  # Default value for instructor reference
                    elif instructor_reference:
                        # Check if the instructor reference number exists in the database and corresponds to an instructor
                        cursor.execute("SELECT COUNT(*) FROM aaas.user WHERE reference_number = %s AND role = 2", [instructor_reference])
                        if cursor.fetchone()[0] == 0:
                            instructor_reference = '1234'  # Set to default if invalid
                    else:
                        return JsonResponse({'error': 'Please provide the instructor reference number.'})

                    cursor.execute(
                        "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number, field, degree) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)",
                        [name, email, password, profile_photo, 'Y', 3, instructor_reference, field, degree]
                    )
                elif role == 'instructor':
                    confirm_password = data.get('password')
                    if confirm_password != password:
                        return JsonResponse({'error': 'Password and confirm password do not match.'})

                    reference_number = ''.join(random.choices('0123456789', k=6))  # Generate reference number for instructor

                    cursor.execute(
                        "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
                        [name, email, password, profile_photo, 'Y', 2, reference_number]
                    )
                elif role == 'admin':
                    confirm_password = data.get('password')
                    if confirm_password != password:
                        return JsonResponse({'error': 'Password and confirm password do not match.'})

                    reference_number = ''.join(random.choices('0123456789', k=6))  # Generate reference number for admin

                    cursor.execute(
                        "INSERT INTO aaas.user (full_name, email, password, photo, status, role, time, reference_number) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)",
                        [name, email, password, profile_photo, 'Y', 1, reference_number]
                    )

                    # Send email with reference number to the new admin
                    send_mail(
                        'Your Admin Reference Number',
                        f'Hello {name},\n\nYour admin reference number is: {reference_number}\n\nBest regards,\nThe Data Tech Labs Team',
                        'pr@thedatatechlabs.com',  # Replace with your email address
                        [email],
                        fail_silently=False,
                    )

                # Get the auto-generated user_id
                user_id = cursor.lastrowid

                # Insert user_id into user_meta table where role is 3 (for students)
                if role == 'student':
                    cursor.execute(
                        "INSERT INTO aaas.user_meta (user_id) VALUES (%s)",
                        [user_id]
                    )

                return JsonResponse({'success': 'User registered successfully.'})
            except IntegrityError as e:
                return JsonResponse({'error': f'An error occurred during registration. Please try again later. Details: {str(e)}'})

    return JsonResponse({'error': 'Invalid request method. Please use POST method for registration.'})

