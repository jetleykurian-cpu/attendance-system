# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from django.db.models import Count
from student_management_app.EmailBackEnd import EmailBackEnd
from .models import Parent, AttendanceReport, StudentResult

def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    email = request.POST.get('email')
    password = request.POST.get('password')

    from student_management_app.EmailBackEnd import EmailBackEnd
    backend = EmailBackEnd()
    user = backend.authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user, backend='student_management_app.EmailBackEnd.EmailBackEnd')

        if user.user_type == '1':
            return redirect('admin_home')
        elif user.user_type == '2':
            return redirect('staff_home')
        elif user.user_type == '3':
            return redirect('student_home')
        elif user.user_type == '4':
            return redirect('parent_home')
    else:
        messages.error(request, "Invalid Login Credentials!")
        return redirect('login')





def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Parent, Attendance, AttendanceReport, StudentResult

@login_required
def parent_home(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student

    attendance_present = AttendanceReport.objects.filter(
        student_id=student,
        status=True
    ).count()

    results = StudentResult.objects.filter(student_id=student)

    return render(request, "parent_template/parent_home.html", {
        "student": student,
        "attendance_count": attendance_present,
        "results": results,
    })


@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student

    attendance = AttendanceReport.objects.filter(student_id=student)
    results = StudentResult.objects.filter(student_id=student)

    return render(request, "parent_template/parent_dashboard.html", {
        "student": student,
        "attendance": attendance,
        "results": results
    })


@login_required
def monthly_attendance(request):
    parent = Parent.objects.get(user=request.user)
    student = parent.student

    current_month = datetime.date.today().month

    total_classes = AttendanceReport.objects.filter(
        student_id=student,
        attendance_id__attendance_date__month=current_month
    ).count()

    present_classes = AttendanceReport.objects.filter(
        student_id=student,
        attendance_id__attendance_date__month=current_month,
        status=True
    ).count()

    percentage = (present_classes / total_classes * 100) if total_classes else 0

    return render(request, "parent_template/monthly_attendance.html", {
        "total": total_classes,
        "present": present_classes,
        "percentage": round(percentage, 2)
    })


@login_required
def login_redirect(request):
    if request.user.user_type == "1":
        return redirect("admin_home")
    elif request.user.user_type == "2":
        return redirect("staff_home")
    elif request.user.user_type == "3":
        return redirect("student_home")
    elif request.user.user_type == "4":
        return redirect("parent_home")
    else:
        return redirect("logout")




