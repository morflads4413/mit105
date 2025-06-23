from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Appointment

def homepage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/dashboard/')
        else:
            return redirect('/appointments/')
    
    return render(request, 'appointments/homepage.html')

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Appointment.objects.all()
        # Since student is now a CharField, we can't filter by user directly
        # For now, show all appointments to non-admin users
        return Appointment.objects.all()
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect admin users to dashboard
        if request.user.is_superuser:
            return redirect('/dashboard/')
        return super().dispatch(request, *args, **kwargs)

class AppointmentCreateView(CreateView):
    model = Appointment
    fields = ['student', 'contact_number', 'date', 'time']
    template_name = 'appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.now().date()
        return context

    def form_valid(self, form):
        # Get the selected date and time
        selected_date = form.cleaned_data['date']
        selected_time = form.cleaned_data['time']
        contact_number = form.cleaned_data.get('contact_number', '')
        
        # Validate mobile number (exactly 11 digits)
        if contact_number:
            # Remove any non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, contact_number))
            if len(digits_only) != 11:
                form.add_error('contact_number', 'Mobile number must be exactly 11 digits.')
                return self.form_invalid(form)
        
        # Check if date is today or in the future
        today = datetime.now().date()
        if selected_date < today:
            form.add_error('date', 'Appointments cannot be booked for past dates.')
            return self.form_invalid(form)
        
        # If booking for today, check if it's at least 2 hours in advance
        if selected_date == today:
            current_time = datetime.now().time()
            two_hours_later = (datetime.now() + timedelta(hours=2)).time()
            if selected_time <= two_hours_later:
                form.add_error('time', 'Same-day appointments must be booked at least 2 hours in advance.')
                return self.form_invalid(form)
        
        # Check if time is during available time slots
        # Morning session: 8:00 AM - 12:00 PM
        # Afternoon session: 1:00 PM - 5:00 PM
        morning_start = datetime.strptime('08:00', '%H:%M').time()
        morning_end = datetime.strptime('12:00', '%H:%M').time()
        afternoon_start = datetime.strptime('13:00', '%H:%M').time()
        afternoon_end = datetime.strptime('17:00', '%H:%M').time()
        
        is_valid_time = (
            (morning_start <= selected_time <= morning_end) or
            (afternoon_start <= selected_time <= afternoon_end)
        )
        
        if not is_valid_time:
            form.add_error('time', 'Appointments are only available during Morning (8:00 AM - 12:00 PM) and Afternoon (1:00 PM - 5:00 PM) sessions.')
            return self.form_invalid(form)
        
        return super().form_valid(form)

class AppointmentSuccessView(TemplateView):
    template_name = 'appointments/appointment_success.html'

@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect admin users to dashboard, others to appointment list
                if user.is_superuser:
                    return redirect('/dashboard/')
                else:
                    return redirect('/appointments/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/')
    
    # Get current date and time
    today = datetime.now().date()
    current_month = today.month
    current_year = today.year
    
    # Statistics
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    approved_appointments = Appointment.objects.filter(status='approved').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    rejected_appointments = Appointment.objects.filter(status='rejected').count()
    
    # Today's appointments
    today_appointments = Appointment.objects.filter(date=today).count()
    
    # This month's appointments
    month_appointments = Appointment.objects.filter(
        date__year=current_year,
        date__month=current_month
    ).count()
    
    # Recent appointments (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_appointments = Appointment.objects.filter(
        date__gte=week_ago
    ).order_by('-created_at')[:5]
    
    # Upcoming appointments (next 7 days)
    week_ahead = today + timedelta(days=7)
    upcoming_appointments = Appointment.objects.filter(
        date__gte=today,
        date__lte=week_ahead
    ).order_by('date', 'time')[:5]
    
    # Status distribution
    status_distribution = Appointment.objects.values('status').annotate(
        count=Count('status')
    ).order_by('status')
    
    # Top counselors by appointment count
    top_counselors = User.objects.filter(
        counselor_appointments__isnull=False
    ).annotate(
        appointment_count=Count('counselor_appointments')
    ).order_by('-appointment_count')[:5]
    
    # Top students by appointment count
    top_students = Appointment.objects.values('student').annotate(
        appointment_count=Count('id')
    ).order_by('-appointment_count')[:5]
    
    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'completed_appointments': completed_appointments,
        'rejected_appointments': rejected_appointments,
        'today_appointments': today_appointments,
        'month_appointments': month_appointments,
        'recent_appointments': recent_appointments,
        'upcoming_appointments': upcoming_appointments,
        'status_distribution': status_distribution,
        'top_counselors': top_counselors,
        'top_students': top_students,
        'today': today,
    }
    
    return render(request, 'appointments/admin_dashboard.html', context)
