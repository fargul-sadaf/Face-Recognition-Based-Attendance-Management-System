from django.shortcuts import render
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.messages.views import SuccessMessageMixin

import face_recognition

from .models import MarkedOutUser
import face_recognition
import cv2
from django.utils import timezone
from django.core.files.base import ContentFile
import numpy as np
import os
from io import BytesIO
from PIL import Image
import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import csv

from django.contrib.auth.decorators import login_required

from .models import Employee, MarkedInUser,MarkedOutUser
from django.db import models


import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Employee, MarkedInUser
import face_recognition
import numpy as np





@csrf_exempt
@login_required
def admin_dashboard(request):
    employees = Employee.objects.all()
    marked_in_records = MarkedInUser.select_related('user').all()
    marked_out_records = MarkedOutUser.select_related('user').all()
    return render(request, 'admin_dashboard.html', {'employees': employees, 'marked_in_records': marked_in_records, 'marked_out_records': marked_out_records})

@csrf_exempt
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Email', 'Mobile', 'Division'])
    for emp in Employee.objects.all():
        writer.writerow([emp.employee_id, emp.employee_name, emp.email, emp.mobile, emp.division])
    return response

@csrf_exempt
def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def register_employee(request):
    if request.method == 'POST':
        name = request.POST.get('employee_name')
        emp_id = request.POST.get('employee_id')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        division = request.POST.get('division')
        uploaded_image = request.FILES.get('employee_image')
        captured_face_data = request.POST.get('captured_face')

        # Create employee instance
        employee = Employee(
            employee_name=name,
            employee_id=emp_id,
            email=email,
            mobile=mobile,
            division=division
        )

        # Save uploaded or captured image
        if uploaded_image:
            employee.face_image = uploaded_image
        elif captured_face_data:
            format, imgstr = captured_face_data.split(';base64,')
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{emp_id}_captured.jpg")
            employee.face_image = image_data
        else:
            messages.error(request, "No image provided.")
            return redirect('register')

        employee.save()
        messages.success(request, "Employee registered successfully!")
        return redirect('register')

    return render(request, 'register.html')

from django.core.files.base import ContentFile
import base64

def image_bytes_to_file(image_bytes, filename):
    return ContentFile(image_bytes, name=filename)

@csrf_exempt
def mark_out(request):
    if request.method == "POST":
        emp_id = request.POST.get("employee_id")
        face_data = request.POST.get("captured_face")

        if not emp_id or not face_data:
            messages.error(request, "Missing data.")
            return redirect("dashboard")

        try:
            employee = Employee.objects.get(employee_id=emp_id)
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found.")
            return redirect("dashboard")

        # Decode base64 image
        format, imgstr = face_data.split(';base64,')
        decoded_image = base64.b64decode(imgstr)
        image_file = ContentFile(decoded_image, name=f"{emp_id}_markout.jpg")

        # Load captured face
        captured_img = face_recognition.load_image_file(io.BytesIO(decoded_image))
        captured_encodings = face_recognition.face_encodings(captured_img)

        if not captured_encodings:
            messages.error(request, "No face detected in captured image.")
            return redirect("dashboard")

        # Load registered face
        registered_img = face_recognition.load_image_file(employee.face_image.path)
        registered_encodings = face_recognition.face_encodings(registered_img)

        if not registered_encodings:
            messages.error(request, "No face found in registered image.")
            return redirect("dashboard")

        match = face_recognition.compare_faces([registered_encodings[0]], captured_encodings[0])[0]

        if match:
            MarkedOutUser.objects.create(user=employee, face_image=image_file)
            messages.success(request, "Attendance marked successfully. Goodbye!")
        else:
            messages.error(request, "Face mismatch. Employee not registered.")
        return redirect("dashboard")
    return render(request, "mark_out.html")

@csrf_exempt
def mark_in(request):
    if request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        captured_data = request.POST.get('captured_face')
        if not emp_id or not captured_data:
            messages.error(request, "Missing data!")
            return redirect('mark_in')
        try:
            employee = Employee.objects.get(employee_id=emp_id)
        except Employee.DoesNotExist:
            messages.error(request, "Employee ID not found.")
            return redirect('mark_in')

        # Decode the captured image
        format, imgstr = captured_data.split(';base64,')
        img_data = base64.b64decode(imgstr)
        image_file = ContentFile(img_data, name=f'{emp_id}_markin.jpg')

        # Load registered face
        registered_image = face_recognition.load_image_file(employee.face_image.path)
        registered_encoding = face_recognition.face_encodings(registered_image)

        if not registered_encoding:
            messages.error(request, "No face found in registered image.")
            return redirect('mark_in')

        registered_encoding = registered_encoding[0]

        # Load captured face
        img = Image.open(io.BytesIO(img_data))
        captured_image_np = np.array(img)
        captured_encoding = face_recognition.face_encodings(captured_image_np)

        if not captured_encoding:
            messages.error(request, "No face found in captured image.")
            return redirect('mark_in')

        captured_encoding = captured_encoding[0]

        # Compare faces
        result = face_recognition.compare_faces([registered_encoding], captured_encoding)[0]

        if result:
            MarkedInUser.objects.create(employee=employee, captured_image=image_file)
            messages.success(request, f"✅ {employee.employee_name} marked in successfully at {timezone.now().strftime('%H:%M:%S')}")
        else:
            messages.error(request, "❌ Face doesn't match with registered image.")
        
        return redirect('mark_in')

    return render(request, 'mark_in.html')







# views.py







from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Only admin users allowed
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not authorized'})

    return render(request, 'admin_login.html')



from django.shortcuts import render
from .models import Employee, MarkedInUser, MarkedOutUser
from django.db.models import OuterRef, Subquery
@login_required(login_url='admin_login')
def admin_dashboard(request):
    employees = Employee.objects.all()

    # Join IN and OUT by employee
    attendance_data = []
    for employee in employees:
        mark_in = MarkedInUser.objects.filter(employee=employee).order_by('-marked_in_time').first()
        mark_out = MarkedOutUser.objects.filter(user=employee).order_by('-marked_out_time').first()
        attendance_data.append({
            'employee': employee,
            'marked_in': mark_in.marked_in_time if mark_in else None,
            'marked_out': mark_out.marked_out_time if mark_out else None,
            'in_image': mark_in.captured_image.url if mark_in else None,
            'out_image': mark_out.face_image.url if mark_out else None
        })

    return render(request, 'admin_dashboard.html', {
        'employees': employees,
        'attendance_data': attendance_data
    })








@csrf_exempt
def export_attendance_csv(request):
    # Create HttpResponse with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Mobile', 'Division', 'Marked In Time', 'Marked Out Time'])

    employees = Employee.objects.all()

    for emp in employees:
        mark_in = MarkedInUser.objects.filter(employee=emp).order_by('-marked_in_time').first()
        mark_out = MarkedOutUser.objects.filter(user=emp).order_by('-marked_out_time').first()

        writer.writerow([
            emp.employee_id,
            emp.employee_name,
            emp.mobile,
            emp.division,
            mark_in.marked_in_time.strftime('%Y-%m-%d %H:%M:%S') if mark_in else '',
            mark_out.marked_out_time.strftime('%Y-%m-%d %H:%M:%S') if mark_out else ''
        ])

    return response


