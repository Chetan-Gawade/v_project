# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def get_exam_questions(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator, q.questions_id, q.description, q.marks as question_marks
#                 FROM exams e
#                 INNER JOIN user u ON e.creator = u.user_id
#                 INNER JOIN exam_question_set eqs ON e.id = eqs.id
#                 INNER JOIN questions q ON eqs.questions_id = q.questions_id
#             """)
#             exam_data = cursor.fetchall()  # Fetch all rows
 
#             if exam_data:
#                 exams = {}
#                 for exam_row in exam_data:
#                     id, title, start_date, marks, duration, creator, questions_id, description, question_marks = exam_row
#                     if id not in exams:
#                         exams[id] = {
#                             'exam_id': id,
#                             'title': title,
#                             'start_date': start_date.strftime("%Y-%m-%d"),
#                             'marks': 0,  # Initialize marks to 0
#                             'duration': duration,
#                             'creator': creator,
#                             'questions': [],
#                             'total_marks': 0  # Initialize total marks
#                         }
#                     exams[id]['questions'].append({
#                         'questions_id': questions_id,
#                         'questions': description,
#                         'marks': question_marks
#                     })
#                     exams[id]['total_marks'] += question_marks  # Add question marks to total marks
#                     exams[id]['marks'] = exams[id]['total_marks']  # Update marks with total marks

#                 return JsonResponse({'exams': list(exams.values())})
#             else:
#                 return JsonResponse({'error': 'No data found in the exams table'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)





# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def get_exam_questions(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator, q.questions_id, q.description, q.marks as question_marks
#                 FROM exams e
#                 INNER JOIN user u ON e.creator = u.user_id
#                 INNER JOIN exam_question_set eqs ON e.id = eqs.id
#                 INNER JOIN questions q ON eqs.questions_id = q.questions_id
#             """)
#             exam_data = cursor.fetchall()  # Fetch all rows
 
#             if exam_data:
#                 exams = {}
#                 for exam_row in exam_data:
#                     id, title, start_date, marks, duration, creator, questions_id, description, question_marks = exam_row
#                     if id not in exams:
#                         exams[id] = {
#                             'exam_id': id,
#                             'title': title,
#                             'start_date': start_date.strftime("%Y-%m-%d") if start_date else None,  # Modified line
#                             'marks': 0,  # Initialize marks to 0
#                             'duration': duration,
#                             'creator': creator,
#                             'questions': [],
#                             'total_marks': 0  # Initialize total marks
#                         }
#                     exams[id]['questions'].append({
#                         'questions_id': questions_id,
#                         'questions': description,
#                         'marks': question_marks
#                     })
#                     exams[id]['total_marks'] += question_marks  # Add question marks to total marks
#                     exams[id]['marks'] = exams[id]['total_marks']  # Update marks with total marks

#                 return JsonResponse({'exams': list(exams.values())})
#             else:
#                 return JsonResponse({'error': 'No data found in the exams table'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def get_exam_questions(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator, q.questions_id, q.description, q.marks as question_marks
#                 FROM exams e
#                 INNER JOIN user u ON e.creator = u.user_id
#                 INNER JOIN exam_question_set eqs ON e.id = eqs.id
#                 INNER JOIN questions q ON eqs.questions_id = q.questions_id
#             """)
#             exam_data = cursor.fetchall()  # Fetch all rows
 
#             if exam_data:
#                 exams = {}
#                 for exam_row in exam_data:
#                     id, title, start_date, marks, duration, creator, questions_id, description, question_marks = exam_row
#                     if id not in exams:
#                         exams[id] = {
#                             'exam_id': id,
#                             'title': title,
#                             'start_date': start_date.strftime("%Y-%m-%d") if start_date else None,
#                             'marks': 0,
#                             'duration': duration,
#                             'creator': creator,
#                             'questions': [],
#                             'total_marks': 0
#                         }
#                     exams[id]['questions'].append({
#                         'questions_id': questions_id,
#                         'questions': description,
#                         'marks': question_marks
#                     })
#                     exams[id]['total_marks'] += question_marks
#                     exams[id]['marks'] = exams[id]['total_marks']  # Assign total_marks to marks

#                 return JsonResponse({'exams': list(exams.values())})
#             else:
#                 return JsonResponse({'error': 'No data found in the exams table'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)





#  *********** previous working code below  *******************

# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def get_exam_questions(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
       
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator, q.questions_id, q.description, q.marks as question_marks
#                 FROM exams e
#                 INNER JOIN user u ON e.creator = u.user_id
#                 INNER JOIN exam_question_set eqs ON e.id = eqs.id
#                 INNER JOIN questions q ON eqs.questions_id = q.questions_id
#             """)
#             exam_data = cursor.fetchall()  # Fetch all rows
 
#             if exam_data:
#                 exams = {}
#                 for exam_row in exam_data:
#                     id, title, start_date, marks, duration, creator, questions_id, description, question_marks = exam_row
#                     if id not in exams:
#                         exams[id] = {
#                             'exam_id': id,
#                             'title': title,
#                             'start_date': start_date.strftime("%Y-%m-%d") if start_date else None,
#                             'marks': 0,
#                             'duration': duration,
#                             'creator': creator,
#                             'questions': [],
#                             'total_marks': 0
#                         }
#                     exams[id]['questions'].append({
#                         'questions_id': questions_id,
#                         'questions': description,
#                         'marks': question_marks
#                     })
#                     exams[id]['total_marks'] += question_marks
#                     exams[id]['marks'] = exams[id]['total_marks']  # Assign total_marks to marks

#                 # Update marks in the exams table
#                 for exam_id, exam_info in exams.items():
#                     update_marks_query = """
#                         UPDATE exams 
#                         SET marks = %s 
#                         WHERE id = %s
#                     """
#                     cursor.execute(update_marks_query, (exam_info['marks'], exam_id))

#                 return JsonResponse({'exams': list(exams.values())})
#             else:
#                 return JsonResponse({'error': 'No data found in the exams table'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)



# Sufiyan code below ... **********4/06/24

import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_exam_questions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        creator_id = data.get('user_id')
        if not creator_id:
            return JsonResponse({'error': 'creator_id is required in the request body'}, status=400)
        
        try:
            creator_id = int(creator_id)
        except ValueError:
            return JsonResponse({'error': 'creator_id must be an integer'}, status=400)
       
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.id, e.title, e.start_date, e.marks, e.duration, u.Full_name as creator, q.questions_id, q.description, q.marks as question_marks
                FROM exams e
                INNER JOIN user u ON e.creator = u.user_id
                INNER JOIN exam_question_set eqs ON e.id = eqs.id
                INNER JOIN questions q ON eqs.questions_id = q.questions_id
                WHERE e.creator = %s
            """, [creator_id])
            exam_data = cursor.fetchall()  # Fetch all rows
 
            if exam_data:
                exams = {}
                for exam_row in exam_data:
                    id, title, start_date, marks, duration, creator, questions_id, description, question_marks = exam_row
                    if id not in exams:
                        exams[id] = {
                            'exam_id': id,
                            'title': title,
                            'start_date': start_date.strftime("%Y-%m-%d") if start_date else None,
                            'marks': 0,
                            'duration': duration,
                            'creator': creator,
                            'questions': [],
                            'total_marks': 0
                        }
                    exams[id]['questions'].append({
                        'questions_id': questions_id,
                        'questions': description,
                        'marks': question_marks
                    })
                    exams[id]['total_marks'] += question_marks
                    exams[id]['marks'] = exams[id]['total_marks']  # Assign total_marks to marks

                # Update marks in the exams table
                for exam_id, exam_info in exams.items():
                    update_marks_query = """
                        UPDATE exams 
                        SET marks = %s 
                        WHERE id = %s
                    """
                    cursor.execute(update_marks_query, (exam_info['marks'], exam_id))

                return JsonResponse({'exams': list(exams.values())})
            else:
                return JsonResponse({'error': f'No exams found for creator with ID {creator_id}'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)