from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime, timedelta, date
from .models import Appointment
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.conf import settings

# Add a default overall slot limit (can be overridden in settings or via admin)
DEFAULT_OVERALL_SLOT_LIMIT = getattr(settings, 'OVERALL_SLOT_LIMIT', 10)

def get_overall_slot_limit():
    return getattr(settings, 'OVERALL_SLOT_LIMIT', DEFAULT_OVERALL_SLOT_LIMIT)

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
        slot_limit = get_overall_slot_limit()
        slot_end_date = getattr(settings, 'SLOT_LIMIT_END_DATE', '')
        # Only count appointments up to the end date
        if slot_end_date:
            appointments_in_range = Appointment.objects.filter(date__gte=datetime.now().date(), date__lte=slot_end_date)
        else:
            appointments_in_range = Appointment.objects.filter(date__gte=datetime.now().date())
        num_appointments = appointments_in_range.count()
        remaining_slots = max(slot_limit - num_appointments, 0)
        context['remaining_slots'] = remaining_slots
        context['overall_slot_limit'] = slot_limit
        context['slot_start_date'] = ''
        context['slot_end_date'] = slot_end_date
        return context

    def form_valid(self, form):
        selected_date = form.cleaned_data['date']
        slot_limit = get_overall_slot_limit()
        slot_start_date = getattr(settings, 'SLOT_LIMIT_START_DATE', '')
        slot_end_date = getattr(settings, 'SLOT_LIMIT_END_DATE', '')
        if slot_start_date and slot_end_date:
            total_appointments = Appointment.objects.filter(date__gte=slot_start_date, date__lte=slot_end_date).count()
        else:
            total_appointments = 0
        if total_appointments >= slot_limit:
            form.add_error('date', 'No more slots available for the allowed range. Please contact the administrator.')
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
    num_recent_appointments = recent_appointments.count()
    
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
    
    overall_slot_limit = get_overall_slot_limit()
    slot_end_date = getattr(settings, 'SLOT_LIMIT_END_DATE', '')
    # Only count appointments up to the end date
    if slot_end_date:
        appointments_in_range = Appointment.objects.filter(date__gte=today, date__lte=slot_end_date)
    else:
        appointments_in_range = Appointment.objects.filter(date__gte=today)
    num_appointments = appointments_in_range.count()
    remaining_slots = max(overall_slot_limit - num_appointments, 0)
    
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
        'current_slot_limit': overall_slot_limit,
        'remaining_slots': remaining_slots,
        'num_recent_appointments': num_recent_appointments,
        'slot_start_date': '',
        'slot_end_date': slot_end_date,
        'overall_slot_limit': overall_slot_limit,
    }
    
    return render(request, 'appointments/admin_dashboard.html', context)

@login_required
@require_POST
def approve_appointment(request, appointment_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to approve appointments.")
    try:
        appointment = Appointment.objects.get(id=appointment_id, status='pending')
        appointment.status = 'approved'
        appointment.save()
    except Appointment.DoesNotExist:
        pass  # Optionally handle error
    return redirect('admin_dashboard')

@login_required
def set_daily_slot_limit(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to set slot limits.")
    if request.method == 'POST':
        try:
            new_limit = int(request.POST.get('slot_limit'))
            end_date = request.POST.get('end_date')
            # Save to settings (or a model in a real app)
            settings.OVERALL_SLOT_LIMIT = new_limit
            settings.SLOT_LIMIT_END_DATE = end_date
        except Exception:
            pass
        return redirect('admin_dashboard')
    current_limit = get_overall_slot_limit()
    end_date = getattr(settings, 'SLOT_LIMIT_END_DATE', '')
    today = date.today().isoformat()
    return render(request, 'appointments/set_slot_limit.html', {
        'current_limit': current_limit,
        'end_date': end_date,
        'today': today,
    })
