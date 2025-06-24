from django.urls import path
from .views import homepage, AppointmentListView, AppointmentCreateView, AppointmentSuccessView, custom_logout, custom_login, admin_dashboard, approve_appointment, set_daily_slot_limit

urlpatterns = [
    path('', homepage, name='homepage'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('success/', AppointmentSuccessView.as_view(), name='appointment_success'),
    path('logout/', custom_logout, name='custom_logout'),
    path('login/', custom_login, name='custom_login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('appointments/<int:appointment_id>/approve/', approve_appointment, name='approve_appointment'),
    path('set-slot-limit/', set_daily_slot_limit, name='set_daily_slot_limit'),
] 