from django.contrib import admin
from .models import Employee,Attendance, MarkedInUser, MarkedOutUser  # Assuming you have these models

# Register your models here.


# admin.site.register(CapturedUserIN)

admin.site.register(Employee)

admin.site.register(MarkedInUser)  # Assuming you want to register MarkedInUser as well

admin.site.register(MarkedOutUser)  # Assuming you want to register MarkedOutUser as well


admin.site.register(Attendance)
