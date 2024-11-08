import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db import connection

def notify_selected_students(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            
            # Extract relevant information
            title = data.get('title')
            start_date = data.get('start_date')
            time = data.get('time')
            
            # Get the list of selected student IDs
            selected_students = data.get('select_students')
            if not selected_students:
                return JsonResponse({'error': 'No students selected'}, status=400)
            
            # Convert the comma-separated string to a list of integers
            student_ids = [int(id) for id in selected_students.split(',')]
            
            # Fetch email addresses from the database
            with connection.cursor() as cursor:
                # Construct a parameterized query with the right number of placeholders
                placeholders = ', '.join(['%s'] * len(student_ids))
                query = f"SELECT user_id, email FROM user WHERE user_id IN ({placeholders})"
                
                # Execute the query with student IDs as parameters
                cursor.execute(query, student_ids)
                students = cursor.fetchall()
            
            # If no matching students found
            if not students:
                return JsonResponse({'error': 'No matching students found'}, status=404)
            
            # Prepare email details
            subject = f"Invitation: {title}"
            message = f'''
            Dear Student,

            You have been selected to participate in the event: {title}
            Date: {start_date}
            Time: {time}

            Please log in to your account for more details.

            Best regards,
            Your Institution
            '''
            from_email = 'pr@thedatatechlabs.com'
            
            # Send email to each student
            for student_id, email in students:
                to_email = [email]
                try:
                    send_mail(
                        subject,
                        message,
                        from_email,
                        to_email,
                        fail_silently=False
                    )
                    print(f"Email sent successfully to student {student_id} at {email}")
                except Exception as e:
                    print(f"Error sending email to student {student_id} at {email}: {e}")
            
            # Return success response
            return JsonResponse({
                'message': 'Emails sent successfully',
                'students_notified': [id for id, _ in students]
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)