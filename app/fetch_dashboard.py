# from django.http import JsonResponse
# from django.db import connection
 
# def fetch_dashboard(request):
#     with connection.cursor() as cursor:
#         # Fetch total number of exams
#         cursor.execute("SELECT COUNT(*) FROM exams;")
#         total_exams = cursor.fetchone()[0]
 
#         # Fetch total number of users with role=3
#         cursor.execute("SELECT COUNT(*) FROM user WHERE role=3;")
#         total_users = cursor.fetchone()[0]
 
#         # Fetch total number of subcategories
#         cursor.execute("SELECT COUNT(*) FROM sub_category;")
#         total_subcategories = cursor.fetchone()[0]
 
#         # Fetch total number of categories
#         cursor.execute("SELECT COUNT(*) FROM category;")
#         total_categories = cursor.fetchone()[0]
 
#         # Fetch total number of questions
#         cursor.execute("SELECT COUNT(*) FROM questions;")
#         total_questions = cursor.fetchone()[0]
 
#         # Fetch total number of students whose percentage is above 50 (Pass)
#         cursor.execute("SELECT COUNT(*) FROM result WHERE marks > 50;")
#         total_pass_students = cursor.fetchone()[0]
 
#         # Fetch category name from category table
#         cursor.execute("SELECT category FROM category;")
#         categories = [row[0] for row in cursor.fetchall()]
 
#         # Fetch subcategory name from sub_category table
#         cursor.execute("SELECT sub_category FROM sub_category;")
#         subcategories = [row[0] for row in cursor.fetchall()]
 
#         # Fetch total number of questions by subcategory
#         cursor.execute("""
#             SELECT
#                 sub_category.sub_category,
#                 COUNT(questions.questions_id) AS total_questions
#             FROM
#                 sub_category
#             LEFT JOIN
#                 questions ON sub_category.sub_category_Id = questions.sub_category_Id
#             GROUP BY
#                 sub_category.sub_category_Id
#             ORDER BY
#                 sub_category.sub_category_Id
#         """)
#         questions_by_subcategory = cursor.fetchall()
 
#     # Serialize the fetched data
#     questions_data = []
#     for row in questions_by_subcategory:
#         questions_data.append({
#             'sub_category': row[0],
#             'total_questions': row[1]
#         })
 
#     # Construct the response data
#     response_data = {
#         "total_exams": total_exams,
#         "total_users": total_users,
#         "total_subcategories": total_subcategories,
#         "total_categories": total_categories,
#         "total_questions": total_questions,
#         "total_pass_students": total_pass_students,
#         "categories": categories,
#         "subcategories": subcategories,
#         "questions_by_subcategory": questions_data
#     }
 
#     # Return the response as JSON
#     return JsonResponse(response_data)
 

from django.http import JsonResponse
from django.db import connection
 
def fetch_dashboard(request):
    with connection.cursor() as cursor:
        # Fetch total number of exams
        cursor.execute("SELECT COUNT(*) FROM exams;")
        total_exams = cursor.fetchone()[0]
 
        # Fetch total number of users with role=3
        cursor.execute("SELECT COUNT(*) FROM user WHERE role=3;")
        total_users = cursor.fetchone()[0]
 
        # Fetch total number of subcategories
        cursor.execute("SELECT COUNT(*) FROM sub_category;")
        total_subcategories = cursor.fetchone()[0]
 
        # Fetch total number of categories
        cursor.execute("SELECT COUNT(*) FROM category;")
        total_categories = cursor.fetchone()[0]
 
        # Fetch total number of questions
        cursor.execute("SELECT COUNT(*) FROM questions;")
        total_questions = cursor.fetchone()[0]
 
        # Fetch total number of students whose percentage is above 50 (Pass)
        cursor.execute("SELECT COUNT(*) FROM result WHERE marks > 50;")
        total_pass_students = cursor.fetchone()[0]
 
        # Fetch categories with total number of questions
        cursor.execute("""
            SELECT
                c.category_id,
                c.category,
                COALESCE(SUM(q.total_questions), 0) AS total_questions
            FROM
                category c
            LEFT JOIN (
                SELECT
                    category_id,
                    COUNT(questions_id) AS total_questions
                FROM
                    questions
                GROUP BY
                    category_id
            ) q ON c.category_id = q.category_id
            GROUP BY
                c.category_id
            ORDER BY
                c.category_id
        """)
        categories_data = cursor.fetchall()
 
        # Fetch subcategories with total number of questions
        cursor.execute("""
            SELECT
                sub_category,
                COALESCE(COUNT(questions.questions_id), 0) AS total_questions
            FROM
                sub_category
            LEFT JOIN
                questions ON sub_category.sub_category_id = questions.sub_category_id
            GROUP BY
                sub_category.sub_category_id
            ORDER BY
                sub_category.sub_category_id
        """)
        subcategories_data = cursor.fetchall()
 
    # Serialize the fetched data
    categories = []
    for row in categories_data:
        categories.append({
            'category_id': row[0],
            'category_name': row[1],
            'total_questions': row[2]
        })
 
    subcategories = [row[0] for row in subcategories_data]
    questions_by_subcategory = [{'sub_category': row[0], 'total_questions': row[1]} for row in subcategories_data]
 
    # Construct the response data
    response_data = {
        "total_exams": total_exams,
        "total_users": total_users,
        "total_subcategories": total_subcategories,
        "total_categories": total_categories,
        "total_questions": total_questions,
        "total_pass_students": total_pass_students,
        "categories": categories,
        "subcategories": subcategories,
        "questions_by_subcategory": questions_by_subcategory
    }
 
    # Return the response as JSON
    return JsonResponse(response_data)
 
 
 
 