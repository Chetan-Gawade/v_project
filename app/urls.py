from django.urls import path
from . import (
    exam,
    registration,
    fetch_user_by_ref_num,
    send_reference_code,
    fetch_users_by_role,
    fetch_all_exams,
    all_sub_category,
    reset_password,
    email_verification,
    verify_code,
    save_photos,
    exam_title,
    result,
    exam_result,
    exam_submission,
    get_exam_details,
    fetch_exam_details,
    add_profile,
    update_profile,
    fetch_profile,
    status,
    upcomingexam,
    status,
    approval_table,
    reg_exam,
    delete_questions,
    show_exam,
    add_roles,
    fetch_questions,
    exam_question_set,
    update_exam,
    fetch_categories,
    add_category,
    add_subcategory,
    fetch_schedule_exam_list,
    fetch_role,
    sub_category_description,
    fetch_question_list,
    login,
    add_quiz,
    true_false,
    add_quiz_detail,
    fetch_user_by_role,
    multiple_details,
    delete_exam,
    show_result,
    student_result_report,
    fetch_dashboard,
    submit_feedback,
    check_face,
)
from .views import detect_face_endpoint

urlpatterns = [
    path("registration/", registration.register_user, name="register_user"),
    # path('fetch_user_by_ref_num/', fetch_user_by_ref_num.fetch_user_by_ref_num,name='fetch_user_by_ref_num'),
    path("login/", login.login_user, name="login_user"),
    path("add_quiz/", add_quiz.fetch_all, name="fetch_all"),
    path("add_quiz_detail/", add_quiz_detail.add_question, name="add_question"),
    path("fetch_user_by_role/", fetch_user_by_role.fetchuser, name="fetchuser"),
    path(
        "multiple_details/", multiple_details.multiple_details, name="multiple_details"
    ),
    path(
        "fetch_users_by_role/",
        fetch_users_by_role.fetch_users_by_role,
        name="fetch_users_by_role",
    ),
    # path('get-users-by-reference-number/', fetch_users_by_role.get_users_by_reference_number, name='get_users_by_reference_number'),
    path(
        "fetch_user_by_ref_num/",
        fetch_user_by_ref_num.fetch_user_by_ref_num,
        name="fetch_user_by_ref_num",
    ),
    path("true_false/", true_false.truefalse, name="truefalse"),
    path("fetch_all_exams/", fetch_all_exams.fetch_all_exams, name="fetch_all_exams"),
    path("exam/", exam.add_exam, name="add_exam"),
    path(
        "fetch_question_list/",
        fetch_question_list.fetch_question_list,
        name="fetch_question_list",
    ),
    path(
        "all_sub_category/",
        all_sub_category.get_subcategories,
        name="get_subcategories",
    ),
    path("sub_category_description/", sub_category_description.fetch, name="fetch"),
    path("fetch_role/", fetch_role.fetch_role, name="fetch_role"),
    path(
        "fetch_schedule_exam_list/",
        fetch_schedule_exam_list.fetch_schedule_exam_list,
        name="fetch_schedule_exam_list",
    ),
    path("add_roles/", add_roles.add_roles, name="add_roles"),
    path("add_category/", add_category.add_category, name="add_category"),
    path("add_subcategory/", add_subcategory.add_subcategory, name="add_subcategory"),
    path("delete_exam/", delete_exam.delete_exam, name="delete_exam"),
    path(
        "exam_question_set/",
        exam_question_set.add_question_to_exam,
        name="add_question_to_exam",
    ),
    path("update_exam/", update_exam.update_exam, name="update_exam"),
    path(
        "fetch_categories/", fetch_categories.fetch_categories, name="fetch_categories"
    ),
    path(
        "fetch_questions/",
        fetch_questions.get_exam_questions,
        name="get_exam_questions",
    ),
    path("upcomingexam/", upcomingexam.get, name="get"),
    path(
        "delete_questions/", delete_questions.delete_questions, name="delete_questions"
    ),
    path("show_exam/", show_exam.get, name="get"),
    path("reg_exam/", reg_exam.exams, name="exams"),
    path("approval_table/", approval_table.pending_exams, name="pending_exams"),
    path("status/", status.approve_exam, name="approve_exam"),
    path("add_profile/", add_profile.add_profile, name="add_profile"),
    path("update_profile/", update_profile.update_profile, name="update_profile"),
    path("fetch_profile/", fetch_profile.fetch_profile, name="fetch_profile"),
    path(
        "get_exam_details/", get_exam_details.get_exam_details, name="get_exam_details"
    ),
    path("save_photos/", save_photos.save_photos, name="save_photos"),
    path(
        "fetch_exam_details/",
        fetch_exam_details.fetch_exam_details,
        name="fetch_exam_details",
    ),
    path("exam_submission/", exam_submission.exam_submission, name="exam_submission"),
    path("result/", result.result, name="result"),
    path("exam_result/", exam_result.exam_result, name="exam_result"),
    path("show_result/", show_result.show_result, name="show_result"),
    path(
        "student_result_report/",
        student_result_report.student_result_report,
        name="student_result_report",
    ),
    path("fetch_dashboard/", fetch_dashboard.fetch_dashboard, name="fetch_dashboard"),
    path("submit_feedback/", submit_feedback.submit_feedback, name="submit_feedback"),
    path("exam_title/", exam_title.user_exam_results, name="user_exam_results"),
    path(
        "email_verification/",
        email_verification.email_verification,
        name="email_verification",
    ),
    path(
        "send_reference_code/",
        send_reference_code.send_reference_code,
        name="send_reference_code",
    ),
    path("verify_code/", verify_code.verify_code, name="verify_code"),
    path("reset_password/", reset_password.reset_password, name="reset_password"),
    path("detect_faces/", detect_face_endpoint, name="detect_faces"),
    path(
        "check_faces/", check_face.check_faces, name="check_faces"
    ),  # Aaryadev Ghosalkar
]

# NEW
# madhura


# ssssssss
