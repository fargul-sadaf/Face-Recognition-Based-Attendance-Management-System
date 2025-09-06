from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

# Manually changed to include UserImages and Attendance models
# class UserImages(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     face_image = models.ImageField(upload_to="static/")
#     name=models.CharField(max_length=100, blank=True, null=True)
    
#     def __str__(self):
#         # return seluser.username.
#         return self.name

# from django.db import models

# class UserImages(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     face_image = models.ImageField(upload_to='faces/')
#     def __str__(self):
#         return self.user.username



# class Attendance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.user.username
    
    
    
# Added manually for attendance marking

# class Attendance(models.Model):
#     employee_name = models.CharField(max_length=100, blank=True, null=True)
#     time_in = models.DateTimeField(null=True, blank=True)
#     time_out = models.DateTimeField(null=True, blank=True)
#     captured_image = models.ImageField(upload_to='attendance/', null=True, blank=True)

#     def __str__(self):
#         return self.employee_name



class Employee(models.Model):
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    division = models.CharField(max_length=50)
    face_image = models.ImageField(upload_to='EmpImages/', null=True, blank=True)  # can be upload or webcam

    def __str__(self):
        return self.employee_name


# class Attendance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     time_in = models.DateTimeField(null=True, blank=True)
#     time_out = models.DateTimeField(null=True, blank=True)
#     captured_image = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.time_in} / {self.time_out}"





# class Attendance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     time_in = models.DateTimeField(null=True, blank=True)
#     time_out = models.DateTimeField(null=True, blank=True)
#     captured_image = models.ImageField(upload_to='attendance/', null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.time_in or self.time_out}"


# class MarkedInUser(models.Model):
#     user = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     face_image = models.ImageField(upload_to='mark_in_images/')
#     marked_in = models.DateTimeField(default=timezone.now) 

#     def __str__(self):
#         return f"{self.user.employee_name} - {self.marked_in}"

class MarkedOutUser(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='marked_out_faces/')
    marked_out_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.employee_name} - {self.marked_out_time}"

class MarkedInUser(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    marked_in_time = models.DateTimeField(default=timezone.now)
    captured_image = models.ImageField(upload_to='marked_in_images/')

    def __str__(self):
        return f"{self.employee.employee_name} marked in at {self.marked_in_time}"



class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    marked_in = models.DateTimeField(null=True, blank=True)
    marked_out = models.DateTimeField(null=True, blank=True)
    # captured_image = models.ImageField(upload_to='attendance_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.employee.employee_name} - Attendance"
