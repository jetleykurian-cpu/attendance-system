from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
import json

from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, StudentResult, Parent, ParentFeedback


def parent_home(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student

    # Counts
    attendance_present = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
    total_attendance = attendance_present + attendance_absent
    results_count = StudentResult.objects.filter(student_id=student.id).count()
    subjects_count = Subjects.objects.filter(course_id=student.course_id).count()

    # New counts
    new_attendance_count = AttendanceReport.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else total_attendance
    new_results_count = StudentResult.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count

    context = {
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_attendance": total_attendance,
        "results_count": results_count,
        "subjects_count": subjects_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_home_template.html", context)


def parent_performance(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student

    # Results
    results = StudentResult.objects.filter(student_id=student.id)

    # Performance data for graph
    subject_names = []
    total_marks = []
    for result in results:
        subject_names.append(result.subject_id.subject_name)
        total_marks.append(result.total_marks())

    attendance_total = AttendanceReport.objects.filter(student_id=student.id).count()
    results_count = results.count()
    new_attendance_count = AttendanceReport.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else attendance_total
    new_results_count = StudentResult.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count

    context = {
        "student": student,
        "results": results,
        "subject_names_json": json.dumps(subject_names),
        "total_marks_json": json.dumps(total_marks),
        "attendance_total": attendance_total,
        "results_count": results_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_performance_template.html", context)


def parent_student_profile(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student
    attendance_total = AttendanceReport.objects.filter(student_id=student.id).count()
    results_count = StudentResult.objects.filter(student_id=student.id).count()
    new_attendance_count = AttendanceReport.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else attendance_total
    new_results_count = StudentResult.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count
    context = {
        "student": student,
        "attendance_total": attendance_total,
        "results_count": results_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_student_profile.html", context)


def parent_view_results(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student
    results = StudentResult.objects.filter(student_id=student.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student.id).count()
    results_count = results.count()
    new_attendance_count = AttendanceReport.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else attendance_total
    new_results_count = StudentResult.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count
    
    # Mark as viewed
    parent.last_viewed_results = timezone.now()
    parent.save()
    
    context = {
        "student": student,
        "results": results,
        "attendance_total": attendance_total,
        "results_count": results_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_view_results.html", context)


def parent_feedback(request):
    parent = Parent.objects.get(user=request.user)
    feedbacks = ParentFeedback.objects.filter(parent_id=parent)
    # Only show subjects that have valid staff assignments (staff exists)
    valid_staff_ids = Staffs.objects.values_list('id', flat=True)
    subjects = Subjects.objects.filter(course_id=parent.student.course_id, staff_id__in=valid_staff_ids)
    attendance_total = AttendanceReport.objects.filter(student_id=parent.student.id).count()
    results_count = StudentResult.objects.filter(student_id=parent.student.id).count()
    new_attendance_count = AttendanceReport.objects.filter(student_id=parent.student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else attendance_total
    new_results_count = StudentResult.objects.filter(student_id=parent.student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count
    context = {
        "feedbacks": feedbacks,
        "subjects": subjects,
        "attendance_total": attendance_total,
        "results_count": results_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_feedback.html", context)


def parent_feedback_save(request):
    if request.method != "POST":
        return redirect('parent_feedback')
    
    parent = Parent.objects.get(user=request.user)
    feedback_type = request.POST.get('feedback_type')
    feedback_text = request.POST.get('feedback')
    
    if feedback_type == 'admin':
        ParentFeedback.objects.create(parent_id=parent, feedback=feedback_text)
    elif feedback_type == 'staff':
        subject_id = request.POST.get('subject')
        subject = Subjects.objects.get(id=subject_id)
        ParentFeedback.objects.create(parent_id=parent, subject_id=subject, feedback=feedback_text)
    
    messages.success(request, "Feedback sent successfully!")
    return redirect('parent_feedback')


@csrf_exempt
def parent_delete_feedback(request):
    feedback_id = request.POST.get('id')
    parent = Parent.objects.get(user=request.user)
    
    try:
        feedback = ParentFeedback.objects.get(id=feedback_id, parent_id=parent)
        feedback.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def parent_view_attendance(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student
    subjects = Subjects.objects.filter(course_id=student.course_id)
    attendance_total = AttendanceReport.objects.filter(student_id=student.id).count()
    results_count = StudentResult.objects.filter(student_id=student.id).count()
    new_attendance_count = AttendanceReport.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_attendance).count() if parent.last_viewed_attendance else attendance_total
    new_results_count = StudentResult.objects.filter(student_id=student.id, created_at__gt=parent.last_viewed_results).count() if parent.last_viewed_results else results_count
    
    # Mark as viewed
    parent.last_viewed_attendance = timezone.now()
    parent.save()
    
    context = {
        "subjects": subjects,
        "attendance_total": attendance_total,
        "results_count": results_count,
        "new_attendance_count": new_attendance_count,
        "new_results_count": new_results_count,
    }
    return render(request, "parent_template/parent_view_attendance.html", context)


@csrf_exempt
def parent_view_attendance_post(request):
    from datetime import datetime, timedelta
    parent = Parent.objects.get(user=request.user)
    student = parent.student
    subject_id = request.POST.get("subject")
    start_date_str = request.POST.get("start_date")
    end_date_str = request.POST.get("end_date")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    
    attendance_dates = []
    current_date = start_date
    while current_date <= end_date:
        # Check if attendance exists for this date
        attendance_report = AttendanceReport.objects.filter(
            student_id=student.id,
            attendance_id__subject_id=subject_id,
            attendance_id__attendance_date=current_date
        ).first()
        if attendance_report:
            status = "Present" if attendance_report.status else "Absent"
        else:
            status = "Pending"
        attendance_dates.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "status": status
        })
        current_date += timedelta(days=1)
    return JsonResponse(attendance_dates, safe=False)