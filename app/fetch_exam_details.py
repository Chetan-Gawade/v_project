import json
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
 
@csrf_exempt
def fetch_exam_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        exam_id = data.get('exam_id')
        user_id = data.get('user_id')
 
        if not exam_id:
            return JsonResponse({'error': 'Missing exam_id parameter'})
 
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT exams.title, exams.start_date, exams.marks, exams.description, exams.time, exams.duration,
                       questions.questions_id, questions.description AS question_description, questions.marks AS question_marks,
                       questions_option.option_id, questions_option.option, questions_option.is_correct,
                       questions.type_id
                FROM exams
                INNER JOIN exam_question_set ON exams.id = exam_question_set.id
                INNER JOIN questions ON exam_question_set.questions_id = questions.questions_id
                INNER JOIN questions_option ON questions.questions_id = questions_option.questions_id
                WHERE exams.id = %s
                """,
                [exam_id]
            )
 
            results = cursor.fetchall()
 
            if not results:
                return JsonResponse({'data': []})
 
            data_dict = {}
            for row in results:
                exam_key = (row[0], str(row[1]), row[2], row[3], str(row[4]), row[5])
                if exam_key not in data_dict:
                    data_dict[exam_key] = {
                        'title': row[0],
                        'start_date': str(row[1]),
                        'marks': row[2],
                        'description': row[3],
                        'time': str(row[4]),
                        'duration': row[5],
                        'questions': [],
                    }
 
                question_id = row[6]
 
                question_exists = any(q['question_id'] == question_id for q in data_dict[exam_key]['questions'])
                if not question_exists:
                    question = {
                        'question_id': question_id,
                        'question_description': row[7],
                        'question_marks': row[8],
                        'type_id': row[12],
                        'options': [],
                    }
                    data_dict[exam_key]['questions'].append(question)
 
                for q in data_dict[exam_key]['questions']:
                    if q['question_id'] == question_id:
                        q['options'].append({
                            'option_id': row[9],
                            'option': row[10],
                            'is_correct': row[11],
                        })
 
            data = list(data_dict.values())
 
            return JsonResponse({'data': data}, safe=False)
 
    return JsonResponse({'error': 'Invalid request method'})
 

# import json
# from django.http import JsonResponse
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def fetch_exam_details(request):
#     if request.method == 'POST':
#         # Log the received parameters for debugging
#         print(json.loads(request.body))

#         data = json.loads(request.body)
#         exam_id = data.get('exam_id')
#         user_id = data.get('user_id')

#         # Check if exam_id is provided
#         if not exam_id:
#             print('Missing exam_id parameter in the request')
#             return JsonResponse({'error': 'Missing exam_id parameter'})

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT exams.title, exams.start_date, exams.marks, exams.description, exams.time, exams.duration,
#                        questions.questions_id, questions.description AS question_description, questions.marks AS question_marks,
#                        questions_option.option_id, questions_option.option, questions_option.is_correct,
#                        questions.type_id  -- Include the type_id column
#                 FROM exams
#                 INNER JOIN exam_question_set ON exams.id = exam_question_set.id
#                 INNER JOIN questions ON exam_question_set.questions_id = questions.questions_id
#                 INNER JOIN questions_option ON questions.questions_id = questions_option.questions_id
#                 WHERE exams.id = %s
#                 """,
#                 [exam_id]
#             )

#             results = cursor.fetchall()

#             # Check if results are empty
#             if not results:
#                 print('No data found for the specified exam_id')
#                 return JsonResponse({'data': []})

#             data_dict = {}
#             for row in results:
#                 exam_key = (row[0], str(row[1]), row[2], row[3], str(row[4]), row[5])
#                 if exam_key not in data_dict:
#                     data_dict[exam_key] = {
#                         'title': row[0],
#                         'start_date': str(row[1]),
#                         'marks': row[2],
#                         'description': row[3],
#                         'time': str(row[4]),
#                         'duration': row[5],
#                         'questions': [],
#                     }

#                 question_id = row[6]

#                 # Check if the question is already added, if not, add it
#                 question_exists = any(q['question_id'] == question_id for q in data_dict[exam_key]['questions'])
#                 if not question_exists:
#                     question = {
#                         'question_id': question_id,
#                         'question_description': row[7],
#                         'question_marks': row[8],
#                         'type_id': row[12],  # Add type_id to the question dictionary
#                         'options': [],
#                     }
#                     data_dict[exam_key]['questions'].append(question)

#                 # Add the option to the corresponding question
#                 for q in data_dict[exam_key]['questions']:
#                     if q['question_id'] == question_id:
#                         q['options'].append({
#                             'option_id': row[9],
#                             'option': row[10],
#                             'is_correct': row[11],
#                         })

#             # Convert dictionary values to a list to get the desired response format
#             data = list(data_dict.values())

#             return JsonResponse({'data': data}, safe=False)

#     return JsonResponse({'error': 'Invalid request method'})
