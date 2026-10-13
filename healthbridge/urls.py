from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [

    # ================= ADMIN =================

    path(
        'admin/',
        admin.site.urls
    ),

    # ================= HOME =================

    path(
        '',
        views.home,
        name='home'
    ),

    # ================= DOCTORS =================

    path(
        'find_doctor/',
        views.find_doctor,
        name='find_doctor'
    ),

    # ================= HOSPITALS =================

    path(
        'hospitals/',
        views.hospitals,
        name='hospitals'
    ),

    path(
        'hospital/<int:hospital_id>/',
        views.hospital_details,
        name='hospital_detail'
    ),

    # ================= APPOINTMENTS =================

    path(
        'appointments/',
        views.appointments,
        name='appointments'
    ),

    path(
        'book_appointment/<int:doctor_id>/',
        views.book_appointment,
        name='book_appointment'
    ),

    # ================= AUTHENTICATION =================

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'forgot_password/',
        views.forgot_password,
        name='forgot_password'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ================= PATIENT DASHBOARD =================

    path(
        'patient_dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    # ================= DOCTOR DASHBOARD =================

    path(
        'doctor_dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),
   
    path(
        'update_appointment_status/<int:appointment_id>/',
         views.update_appointment_status,
         name='update_appointment_status'
    ),
    # ================= DASHBOARD SELECTION =================

    path(
       'dashboard/',
        views.dashboard_selection,
        name='dashboard_selection'
   ),

]