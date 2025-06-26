# 🎓 Guidance Online Appointment System

A modern, user-friendly web application for managing guidance counseling appointments built with Django.

## ✨ Features

- **No Login Required for Students**: Students can book appointments without creating accounts
- **Admin Management**: Administrators can view and manage all appointments
- **Modern UI**: Beautiful, responsive design with glassmorphism effects
- **Real-time Status**: Track appointment status (pending, approved, rejected, completed)
- **Mobile Friendly**: Works perfectly on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Django 5.2.1

### Installation

1. **Clone or download the project**
   ```bash
   cd "Guidance Online Appointment"
   ```

2. **Install Django** (if not already installed)
   ```bash
   python -m pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create test users**
   ```bash
   python manage.py create_test_users
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## 👥 User Types & Access

### Students (No Login Required)
- **Can**: Book appointments by selecting their name from dropdown
- **Cannot**: View appointment history or manage appointments
- **Process**: Fill form → Submit → Get confirmation

### Counselors (Staff Access)
- **Can**: View appointments assigned to them
- **Login**: Use counselor credentials
- **Access**: `/accounts/login/` with counselor username/password

### Administrators (Superuser)
- **Can**: View all appointments, manage users, approve/reject appointments
- **Login**: Use admin credentials
- **Access**: `/admin/` or `/accounts/login/`

## 🔑 Test Credentials

### Students (Password: `student123`)
- `john_doe` - John Doe
- `jane_smith` - Jane Smith
- `mike_johnson` - Mike Johnson
- `sarah_wilson` - Sarah Wilson
- `david_brown` - David Brown

### Counselors (Password: `counselor123`)
- `dr_garcia` - Dr. Maria Garcia
- `dr_rodriguez` - Dr. Carlos Rodriguez
- `ms_thompson` - Ms. Jennifer Thompson

### Admin
- `admin` - (password set during creation)

## 📱 How to Use

### For Students (Booking Appointments)

1. **Visit the homepage** (`http://127.0.0.1:8000/`)
2. **Click "Book Your Appointment Now"**
3. **Fill out the form**:
   - Select your name from the dropdown
   - Choose a counselor
   - Pick date and time
   - Describe your reason for the appointment
4. **Submit the form**
5. **Get confirmation** on the success page

### For Administrators (Managing Appointments)

1. **Login** at `/accounts/login/` with admin credentials
2. **View all appointments** on the dashboard
3. **Manage appointments** through the admin panel at `/admin/`
4. **Update appointment status** (pending → approved/rejected)

## 🎨 Design Features

- **Modern Gradient Background**: Purple/blue theme
- **Glassmorphism Effects**: Translucent cards with backdrop blur
- **Responsive Design**: Works on all screen sizes
- **Smooth Animations**: Hover effects and transitions
- **Status Badges**: Color-coded appointment status
- **Emoji Icons**: Visual appeal and better UX

## 📁 Project Structure

```
Guidance Online Appointment/
├── guidance_appointment_system/    # Main Django project
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main URL configuration
│   └── ...
├── appointments/                   # Main app
│   ├── models.py                   # Appointment model
│   ├── views.py                    # View logic
│   ├── urls.py                     # App URL configuration
│   ├── admin.py                    # Admin interface
│   └── templates/                  # App templates
├── templates/                      # Global templates
│   ├── base.html                   # Base template
│   └── registration/               # Auth templates
├── manage.py                       # Django management
└── README.md                       # This file
```

## 🔧 Customization

### Adding New Users
```bash
python manage.py create_test_users
```

### Changing Colors
Edit the CSS variables in `templates/base.html`:
- Primary color: `#667eea`
- Success color: `#28a745`
- Background gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

### Adding New Fields
1. Modify `appointments/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`

## 🚀 Deployment

For production deployment:

1. **Set DEBUG = False** in `settings.py`
2. **Configure ALLOWED_HOSTS**
3. **Use a production database** (PostgreSQL recommended)
4. **Set up static files** with a web server
5. **Use a production WSGI server** (Gunicorn + Nginx)

## 📞 Support

For issues or questions:
1. Check the Django documentation
2. Review the error logs
3. Ensure all migrations are applied
4. Verify user credentials are correct

## 📄 License

This project is created for educational purposes. Feel free to modify and use as needed.

---

**Happy Counseling! 🎓✨** 