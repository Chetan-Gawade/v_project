from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def fetch_all_exams(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user_id = data.get('user_id')
        else:  # GET method
            user_id = request.GET.get('user_id')

        if user_id is not None:
            exams_list = []
            with connection.cursor() as cursor:
                # Define the query to fetch records from the exams table for a particular user_id
                query = """
                SELECT e.id, e.title, e.start_date, e.description, e.time, e.duration, e.marks, e.rules, u.full_name as creator
                FROM exams e
                INNER JOIN user u ON e.creator = u.user_id
                WHERE e.creator = %s
                """
        
                # Execute the query with the user_id parameter
                cursor.execute(query, [user_id])
 
                # Fetch all records
                exams_data = cursor.fetchall()
 
                # Convert the fetched data into a list of dictionaries
                # exams_list = []
                for exam_data in exams_data:
                    exam_dict = {
                        'id': exam_data[0],  # Renaming exam_id to id
                        'title': exam_data[1],
                        'start_date': str(exam_data[2]),  # Assuming start_date is a datetime object
                        'description': exam_data[3],
                        'time': str(exam_data[4]),  # Assuming time is a time object
                        'duration': exam_data[5],
                        'marks': exam_data[6],
                        'rules': exam_data[7],
                        'creator': exam_data[8]
                    }
    
                    # Fetch questions related to the exam
                    cursor.execute("""
                        SELECT questions.questions_id, questions.description, questions.marks
                        FROM exam_question_set
                        INNER JOIN questions ON exam_question_set.questions_id = questions.questions_id
                        WHERE exam_question_set.id = %s
                    """, [exam_data[0]])
                    exam_questions = cursor.fetchall()
    
                    # Calculate total marks for the exam
                    total_marks = sum(question[2] for question in exam_questions)
    
                    # Append questions and total marks to the exam dictionary
                    exam_dict['questions'] = [{'question_id': q[0], 'description': q[1], 'marks': q[2]} for q in exam_questions]
                    exam_dict['total_marks'] = total_marks
    
                    exams_list.append(exam_dict)
 
        # Return the fetched data as JSON response
        return JsonResponse({'exams': exams_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
