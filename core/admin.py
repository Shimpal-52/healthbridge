from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor, Hospital, Appointment
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Appointment)
