from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Patient, Doctor, Hospital, Appointment


# ================= HOME =================

def home(request):
    return render(request, 'core/home.html')


# ================= FIND DOCTOR =================

def find_doctor(request):
    query = request.GET.get('q', '').strip()

    search_query = query

    if search_query.lower().startswith('dr.'):
        search_query = search_query[3:].strip()

    elif search_query.lower().startswith('dr '):
        search_query = search_query[2:].strip()

    if search_query:
        doctors = Doctor.objects.filter(
            models.Q(name__icontains=search_query) |
            models.Q(specialization__icontains=search_query)
        )
    else:
        doctors = Doctor.objects.all()

    return render(request, 'core/find_doctor.html', {
        'doctors': doctors,
        'query': query
    })


# ================= HOSPITALS =================

def hospitals(request):
    query = request.GET.get('q', '').strip()

    hospitals = Hospital.objects.all()

    if query:
        hospitals = hospitals.filter(
            models.Q(name__icontains=query) |
            models.Q(address__icontains=query)
        )

    return render(request, 'core/hospitals.html', {
        'hospitals': hospitals,
        'query': query
    })


# ================= HOSPITAL DETAILS =================

def hospital_details(request, hospital_id):
    hospital = get_object_or_404(
        Hospital,
        id=hospital_id
    )

    return render(request, 'core/hospital_details.html', {
        'hospital': hospital
    })


# ================= APPOINTMENTS =================

def appointments(request):

    if request.method == 'POST':

        name = request.POST.get('patient_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        doctor_name = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Doctor name se doctor find karo
        if doctor_name:
            doctor_name = doctor_name.replace('Dr. ', '').strip()

        doctor = get_object_or_404(
            Doctor,
            name__icontains=doctor_name
        )

        # Patient create ya existing patient find
        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone
            }
        )

        # Existing patient ki details update
        if not created:
            patient.name = name
            patient.phone = phone
            patient.save()

        # Appointment database me save
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        return redirect('appointments')

    # Existing appointments
    appointments_list = Appointment.objects.all().order_by(
        '-appointment_date'
    )

    # Doctors aur hospitals form ke liye
    doctors = Doctor.objects.all()
    hospitals_list = Hospital.objects.all()

    return render(request, 'core/appointments.html', {
        'appointments': appointments_list,
        'doctors': doctors,
        'hospitals': hospitals_list
    })


# ================= BOOK APPOINTMENT =================

def book_appointment(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Patient create ya existing patient find
        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone
            }
        )

        if not created:
            patient.name = name
            patient.phone = phone
            patient.save()

        # Appointment save
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        return redirect('appointments')

    return render(request, 'core/book_appointment.html', {
        'doctor': doctor
    })


# ================= LOGIN =================

def login_view(request):
    return render(request, 'core/login.html')


# ================= REGISTER =================

def register(request):
    return render(request, 'core/register.html')