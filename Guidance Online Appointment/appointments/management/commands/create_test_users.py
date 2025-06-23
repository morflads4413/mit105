from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create default test users for the guidance appointment system'

    def handle(self, *args, **options):
        # Test Students
        students = [
            {
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@student.edu',
                'password': 'student123'
            },
            {
                'username': 'jane_smith',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@student.edu',
                'password': 'student123'
            },
            {
                'username': 'mike_johnson',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'email': 'mike.johnson@student.edu',
                'password': 'student123'
            },
            {
                'username': 'sarah_wilson',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'email': 'sarah.wilson@student.edu',
                'password': 'student123'
            },
            {
                'username': 'david_brown',
                'first_name': 'David',
                'last_name': 'Brown',
                'email': 'david.brown@student.edu',
                'password': 'student123'
            }
        ]

        # Test Counselors
        counselors = [
            {
                'username': 'dr_garcia',
                'first_name': 'Dr. Maria',
                'last_name': 'Garcia',
                'email': 'maria.garcia@school.edu',
                'password': 'counselor123'
            },
            {
                'username': 'dr_rodriguez',
                'first_name': 'Dr. Carlos',
                'last_name': 'Rodriguez',
                'email': 'carlos.rodriguez@school.edu',
                'password': 'counselor123'
            },
            {
                'username': 'ms_thompson',
                'first_name': 'Ms. Jennifer',
                'last_name': 'Thompson',
                'email': 'jennifer.thompson@school.edu',
                'password': 'counselor123'
            }
        ]

        created_count = 0
        skipped_count = 0

        # Create students
        self.stdout.write('Creating test students...')
        for student_data in students:
            try:
                user, created = User.objects.get_or_create(
                    username=student_data['username'],
                    defaults={
                        'first_name': student_data['first_name'],
                        'last_name': student_data['last_name'],
                        'email': student_data['email'],
                        'is_staff': False,
                        'is_superuser': False
                    }
                )
                if created:
                    user.set_password(student_data['password'])
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created student: {user.get_full_name()} ({user.username})')
                    )
                    created_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Student already exists: {user.get_full_name()} ({user.username})')
                    )
                    skipped_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating student {student_data["username"]}: {str(e)}')
                )

        # Create counselors
        self.stdout.write('\nCreating test counselors...')
        for counselor_data in counselors:
            try:
                user, created = User.objects.get_or_create(
                    username=counselor_data['username'],
                    defaults={
                        'first_name': counselor_data['first_name'],
                        'last_name': counselor_data['last_name'],
                        'email': counselor_data['email'],
                        'is_staff': True,  # Counselors have staff access
                        'is_superuser': False
                    }
                )
                if created:
                    user.set_password(counselor_data['password'])
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created counselor: {user.get_full_name()} ({user.username})')
                    )
                    created_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Counselor already exists: {user.get_full_name()} ({user.username})')
                    )
                    skipped_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating counselor {counselor_data["username"]}: {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} new users'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped {skipped_count} existing users'))
        
        self.stdout.write('\nTest User Credentials:')
        self.stdout.write('Students (password: student123):')
        for student in students:
            self.stdout.write(f'  - {student["username"]} ({student["first_name"]} {student["last_name"]})')
        
        self.stdout.write('\nCounselors (password: counselor123):')
        for counselor in counselors:
            self.stdout.write(f'  - {counselor["username"]} ({counselor["first_name"]} {counselor["last_name"]})')
        
        self.stdout.write('\nAdmin (if created):')
        self.stdout.write('  - admin (password: as set during creation)')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Test users setup completed!')) 