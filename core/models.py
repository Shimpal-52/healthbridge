from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
            return self.name
class Hospital(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
            return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Appointment for {self.patient.name} with Dr. {self.doctor.name} on {self.appointment_date} at {self.appointment_time}"       
     