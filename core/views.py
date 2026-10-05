from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

# ================= APPOINTMENTS =================

@login_required(login_url='login')
def appointments(request):

    # Logged-in user ka Patient record
    patient, created = Patient.objects.get_or_create(
        email=request.user.email,
        defaults={
            'name': request.user.first_name or request.user.username,
            'phone': ''
        }
    )

    # ================= POST =================

    if request.method == 'POST':

        doctor_name = request.POST.get('doctor', '').strip()
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Doctor select nahi kiya
        if not doctor_name:
            messages.error(
                request,
                'Please select a doctor.'
            )
            return redirect('appointments')

        # "Dr. " remove karo
        doctor_name = doctor_name.replace('Dr. ', '').strip()

        # Doctor find karo
        doctor = get_object_or_404(
            Doctor,
            name__icontains=doctor_name
        )

        # Appointment save
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        messages.success(
            request,
            'Appointment booked successfully!'
        )

        return redirect('appointments')

    # ================= GET =================

    appointments_list = Appointment.objects.filter(
        patient=patient
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    doctors = Doctor.objects.all()
    hospitals_list = Hospital.objects.all()

    return render(
        request,
        'core/appointments.html',
        {
            'appointments': appointments_list,
            'doctors': doctors,
            'hospitals': hospitals_list
        }
    )


# ================= BOOK APPOINTMENT =================

@login_required(login_url='login')
def book_appointment(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    if request.method == 'POST':

        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Logged-in user ka Patient record
        patient = get_object_or_404(
            Patient,
            email=request.user.email
        )

        # Appointment save
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        messages.success(
            request,
            'Appointment booked successfully!'
        )

        return redirect('appointments')

    return render(request, 'core/book_appointment.html', {
        'doctor': doctor
    })


# ================= LOGIN =================

def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            messages.error(
                request,
                'Invalid email or password.'
            )

            return render(
                request,
                'core/login.html'
            )

        authenticated_user = authenticate(
            request,
            username=user.username,
            password=password
        )

        if authenticated_user is not None:

            login(
                request,
                authenticated_user
            )

            return redirect('home')

        messages.error(
            request,
            'Invalid email or password.'
        )

    return render(
        request,
        'core/login.html'
    )


# ================= FORGOT PASSWORD =================

def forgot_password(request):
    return render(
        request,
        'core/forgot_password.html'
    )


# ================= REGISTER =================

def register(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Password match check
        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        # Email already registered?
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'This email is already registered.'
            )

            return redirect('register')

        # Django User create
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # Patient record create
        Patient.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        messages.success(
            request,
            'Account created successfully. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'core/register.html'
    )


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    return redirect('login')