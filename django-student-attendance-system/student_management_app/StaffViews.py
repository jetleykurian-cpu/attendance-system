from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from student_management_app.models import (
    CustomUser, Staffs, Courses, Subjects, Students,
    SessionYearModel, Attendance, AttendanceReport,
    LeaveReportStaff, FeedBackStaffs, FeedBackStudent, StudentResult, Parent, ParentFeedback
)
from .forms import AddParentForm


# ================================
# STAFF DASHBOARD
# ================================
def staff_home(request):
    staff = Staffs.objects.get(admin=request.user)
    subjects = Subjects.objects.filter(staff_id=staff)

    course_ids = subjects.values_list("course_id", flat=True).distinct()
    students_count = Students.objects.filter(course_id__in=course_ids).count()
    subject_count = subjects.count()
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()

    leave_count = LeaveReportStaff.objects.filter(staff_id=staff, leave_status=1).count()

    subject_list = []
    attendance_list = []

    for subject in subjects:
        subject_list.append(subject.subject_name)
        attendance_list.append(
            Attendance.objects.filter(subject_id=subject).count()
        )

    students = Students.objects.filter(course_id__in=course_ids)

    student_names = []
    present = []
    absent = []

    for s in students:
        student_names.append(s.admin.get_full_name())
        present.append(AttendanceReport.objects.filter(student_id=s, status=True).count())
        absent.append(AttendanceReport.objects.filter(student_id=s, status=False).count())

    context = {
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_names,
        "attendance_present_list": present,
        "attendance_absent_list": absent,
    }
    return render(request, "staff_template/staff_home_template.html", context)


# ================================
# TAKE ATTENDANCE
# ================================
def staff_take_attendance(request):
    staff = Staffs.objects.get(admin=request.user)
    context = {
        "subjects": Subjects.objects.filter(staff_id=staff),
        "session_years": SessionYearModel.objects.all()
    }
    return render(request, "staff_template/take_attendance_template.html", context)


@csrf_exempt
def save_attendance_data(request):
    try:
        student_data = json.loads(request.POST.get("student_ids"))
        subject = Subjects.objects.get(id=request.POST.get("subject_id"))
        session_year = SessionYearModel.objects.get(id=request.POST.get("session_year_id"))
        attendance_date = request.POST.get("attendance_date")

        if Attendance.objects.filter(
            subject_id=subject,
            attendance_date=attendance_date,
            session_year_id=session_year
        ).exists():
            return HttpResponse("Attendance already taken")

        attendance = Attendance.objects.create(
            subject_id=subject,
            attendance_date=attendance_date,
            session_year_id=session_year
        )

        for s in student_data:
            student = Students.objects.get(admin=s["id"])
            AttendanceReport.objects.get_or_create(
                student_id=student,
                attendance_id=attendance,
                defaults={'status': s["status"]}
            )

        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(str(e))


# ================================
# UPDATE ATTENDANCE
# ================================
def staff_update_attendance(request):
    staff = Staffs.objects.get(admin=request.user)
    context = {
        "subjects": Subjects.objects.filter(staff_id=staff),
        "session_years": SessionYearModel.objects.all()
    }
    return render(request, "staff_template/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):
    try:
        subject_id = request.POST.get("subject")
        session_year_id = request.POST.get("session_year_id")
        staff = Staffs.objects.get(admin=request.user)
        print(f"Debug get_attendance_dates: subject_id={subject_id}, session_year_id={session_year_id}, user={request.user}")
        subject = Subjects.objects.get(id=subject_id, staff_id=staff)
        session_year = SessionYearModel.objects.get(id=session_year_id)
        attendance = Attendance.objects.filter(subject_id=subject, session_year_id=session_year)
        print(f"Debug: found {attendance.count()} attendance records")
        data = [{"id": a.id, "attendance_date": str(a.attendance_date)} for a in attendance]
        return JsonResponse(data, safe=False)
    except Subjects.DoesNotExist:
        print("Debug: Subject not assigned to staff")
        return JsonResponse({"error": "Subject not assigned to you"}, safe=False)
    except Exception as e:
        print(f"Debug: Error {e}")
        return JsonResponse({"error": str(e)}, safe=False)


@csrf_exempt
def get_attendance_student(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    print("🔥 VIEW HIT: get_attendance_student")

    attendance_id = request.POST.get("attendance_date")
    print("🔥 attendance_id:", attendance_id)

    if not attendance_id:
        return JsonResponse({"error": "attendance_id missing"}, safe=False)

    attendance = Attendance.objects.filter(id=attendance_id).first()
    if not attendance:
        return JsonResponse({"error": "Attendance not found"}, safe=False)

    reports = AttendanceReport.objects.filter(attendance_id=attendance)
    print("🔥 reports:", reports.count())

    data = []
    for r in reports:
        data.append({
            "id": r.student_id.admin.id,
            "name": r.student_id.admin.first_name + " " + r.student_id.admin.last_name,
            "status": r.status
        })

    return JsonResponse(data, safe=False)



@csrf_exempt
def update_attendance_data(request):
    try:
        attendance = Attendance.objects.get(id=request.POST.get("attendance_id"))
        students = json.loads(request.POST.get("student_ids"))

        for s in students:
            student = Students.objects.get(admin=s["id"])
            report, _ = AttendanceReport.objects.get_or_create(
                student_id=student,
                attendance_id=attendance
            )
            report.status = s["status"]
            report.save()

        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(str(e))


# ================================
# FEEDBACK
# ================================
def staff_feedback(request):
    staff = Staffs.objects.get(admin=request.user)
    return render(request, "staff_template/staff_feedback_template.html", {
        "feedback_data": FeedBackStaffs.objects.filter(staff_id=staff)
    })


def staff_feedback_save(request):
    if request.method == "POST":
        FeedBackStaffs.objects.create(
            staff_id=Staffs.objects.get(admin=request.user),
            feedback=request.POST.get("feedback_message")
        )
        messages.success(request, "Feedback Sent")
    return redirect("staff_feedback")


@csrf_exempt
def staff_delete_feedback(request):
    feedback_id = request.POST.get('id')
    staff = Staffs.objects.get(admin=request.user)
    
    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id, staff_id=staff)
        feedback.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# ================================
# ADD RESULT
# ================================
def staff_add_result(request):
    staff = Staffs.objects.get(admin=request.user)
    subjects = Subjects.objects.filter(staff_id=staff)

    initial = {
        'student_id': None,
        'subject_id': None,
        'assignment_marks': None,
        'exam_marks': None,
        'assignment_out_of': None,
        'exam_out_of': None,
        'remarks': None,
        'result_id': None,
    }

    if request.GET.get('result_id'):
        try:
            result = StudentResult.objects.get(id=request.GET.get('result_id'))
            initial = {
                'student_id': result.student_id.admin.id,
                'subject_id': result.subject_id.id,
                'assignment_marks': result.assignment_marks,
                'exam_marks': result.exam_marks,
                'assignment_out_of': result.assignment_out_of,
                'exam_out_of': result.exam_out_of,
                'remarks': result.remarks,
                'result_id': result.id,
            }
        except StudentResult.DoesNotExist:
            pass

    results = StudentResult.objects.filter(subject_id__in=subjects).select_related('student_id__admin', 'subject_id')

    context = {
        "subjects": subjects,
        "session_years": SessionYearModel.objects.all(),
        "results": results,
        "initial": initial,
    }
    return render(request, "staff_template/add_result_template.html", context)

@csrf_exempt
@csrf_exempt
def get_students(request):
    try:
        subject_id = request.POST.get("subject")
        session_year_id = request.POST.get("session_year")

        print("🔥 subject:", subject_id)
        print("🔥 session_year:", session_year_id)

        staff = Staffs.objects.get(admin=request.user)
        subject = Subjects.objects.get(
            id=subject_id,
            staff_id=staff
        )

        students = Students.objects.filter(
            course_id=subject.course_id,
            session_year_id=session_year_id
        )

        data = []
        for student in students:
            data.append({
                "id": student.admin.id,
                "name": student.admin.first_name + " " + student.admin.last_name
            })

        print("🔥 students found:", len(data))
        return JsonResponse(data, safe=False)

    except Subjects.DoesNotExist:
        return JsonResponse({"error": "Subject not assigned"}, safe=False)

    except Exception as e:
        print("🔥 ERROR:", e)
        return JsonResponse({"error": str(e)}, safe=False)


def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')

    try:
        student_id = request.POST.get("student_list")
        subject_id = request.POST.get("subject")
        assignment_marks = request.POST.get("assignment_marks")
        exam_marks = request.POST.get("exam_marks")
        assignment_out_of = request.POST.get("assignment_out_of")
        exam_out_of = request.POST.get("exam_out_of")
        remarks = request.POST.get("remarks")

        student = Students.objects.get(admin=student_id)
        subject = Subjects.objects.get(id=subject_id)

        # Check if result already exists
        result, created = StudentResult.objects.get_or_create(
            student_id=student,
            subject_id=subject,
            defaults={
                'assignment_marks': assignment_marks,
                'exam_marks': exam_marks,
                'assignment_out_of': assignment_out_of,
                'exam_out_of': exam_out_of,
                'remarks': remarks
            }
        )

        if not created:
            result.assignment_marks = assignment_marks
            result.exam_marks = exam_marks
            result.assignment_out_of = assignment_out_of
            result.exam_out_of = exam_out_of
            result.remarks = remarks
            result.save()

        messages.success(request, "Result Added Successfully!")
        return redirect('staff_add_result')

    except Exception as e:
        messages.error(request, f"Failed to Add Result: {e}")
        return redirect('staff_add_result')


# ================================
# PROFILE
# ================================
def staff_profile(request):
    return render(request, "staff_template/staff_profile.html", {
        "user": request.user,
        "staff": Staffs.objects.get(admin=request.user)
    })


def staff_profile_update(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        if request.POST.get("password"):
            user.set_password(request.POST.get("password"))
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()

        staff = Staffs.objects.get(admin=user)
        staff.address = request.POST.get("address")
        staff.save()

        messages.success(request, "Profile Updated")
    return redirect("staff_profile")



def staff_add_parent(request):
    edit_parent = None
    if request.GET.get('edit'):
        try:
            edit_parent = Parent.objects.get(id=request.GET.get('edit'))
        except Parent.DoesNotExist:
            messages.error(request, "Parent not found")
            return redirect('staff_manage_parents')
    
    form = AddParentForm()
    if edit_parent:
        form = AddParentForm(initial={
            'username': edit_parent.user.username,
            'email': edit_parent.user.email,
            'first_name': edit_parent.user.first_name,
            'last_name': edit_parent.user.last_name,
            'student_id': edit_parent.student,
        })
    
    context = {
        "form": form,
        "edit_parent": edit_parent,
    }
    return render(request, 'staff_template/add_parent_template.html', context)


def staff_add_parent_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_parent')

    edit_parent_id = request.POST.get('edit_parent_id')
    form = AddParentForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Form validation failed")
        return redirect('staff_add_parent')

    if edit_parent_id:
        # Edit mode
        try:
            parent = Parent.objects.get(id=edit_parent_id)
            user = parent.user
            # Check if username has changed and if new username exists
            if form.cleaned_data['username'] != user.username and CustomUser.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('staff_add_parent')
            # Check if email has changed and if new email exists
            if form.cleaned_data['email'] != user.email and CustomUser.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect('staff_add_parent')

            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()

            parent.student = form.cleaned_data['student_id']
            parent.save()

            messages.success(request, "Parent Updated Successfully!")
            return redirect('staff_manage_parents')
        except Parent.DoesNotExist:
            messages.error(request, "Parent not found")
            return redirect('staff_manage_parents')
    else:
        # Add mode
        if not form.cleaned_data['password']:
            messages.error(request, "Password is required for new parent")
            return redirect('staff_add_parent')

        # Check if username already exists
        if CustomUser.objects.filter(username=form.cleaned_data['username']).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('staff_add_parent')

        # Check if email already exists (optional, since email is not unique in Django by default)
        if CustomUser.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('staff_add_parent')

        try:
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type=4
            )

            # Check if Parent record already exists for this user
            parent, created = Parent.objects.get_or_create(
                user=user,
                defaults={'student': form.cleaned_data['student_id']}
            )
            
            # If Parent already existed, update the student
            if not created:
                parent.student = form.cleaned_data['student_id']
                parent.save()

            messages.success(request, "Parent Added Successfully!")
            return redirect('staff_add_parent')

        except Exception as e:
            messages.error(request, f"Failed to Add Parent ❌ {e}")
            return redirect('staff_add_parent')


def staff_manage_parents(request):
    staff = Staffs.objects.get(admin=request.user)
    subjects = Subjects.objects.filter(staff_id=staff)
    course_ids = subjects.values_list("course_id", flat=True).distinct()
    students = Students.objects.filter(course_id__in=course_ids)
    parents = Parent.objects.filter(student__in=students)
    context = {
        'parents': parents
    }
    return render(request, 'staff_template/manage_parents_template.html', context)


def staff_delete_parent(request, parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        user = parent.user
        parent.delete()
        user.delete()
        messages.success(request, "Parent Deleted Successfully!")
    except Parent.DoesNotExist:
        messages.error(request, "Parent not found!")
    return redirect('staff_manage_parents')


def parent_feedback_message(request):
    staff = Staffs.objects.get(admin=request.user)
    # Show feedbacks sent to subjects assigned to this staff
    # For now, include subjects that have staff_id matching this staff's id
    feedbacks = ParentFeedback.objects.filter(
        subject_id__isnull=False,
        subject_id__staff_id=staff
    )
    return render(request, "staff_template/parent_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def parent_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = ParentFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@csrf_exempt
def staff_delete_parent_feedback(request):
    feedback_id = request.POST.get('id')
    staff = Staffs.objects.get(admin=request.user)
    
    try:
        feedback = ParentFeedback.objects.get(id=feedback_id, subject_id__staff_id=staff)
        feedback.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_student_feedback_message(request):
    staff = Staffs.objects.get(admin=request.user)
    feedbacks = FeedBackStudent.objects.filter(staff_id=staff).select_related('student_id__admin', 'student_id__course_id')
    return render(request, "staff_template/student_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def staff_student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@csrf_exempt
def staff_delete_student_feedback(request):
    feedback_id = request.POST.get('id')
    staff = Staffs.objects.get(admin=request.user)
    
    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id, staff_id=staff)
        feedback.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
