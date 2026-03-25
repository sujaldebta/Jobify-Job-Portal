import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

# Create or get a mock recruiter
recruiter, created = User.objects.get_or_create(
    username='mock_recruiter',
    defaults={
        'email': 'recruiter@example.com',
        'is_recruiter': True,
        'is_seeker': False
    }
)

if created:
    recruiter.set_password('password123')
    recruiter.save()

# Mock jobs data
mock_jobs = [
    {
        'title': 'Senior Frontend Developer',
        'company_name': 'TechFlow Solutions',
        'location': 'Remote / San Francisco',
        'salary_range': '$120k - $160k',
        'job_type': 'Full Time',
        'description': 'We are looking for an experienced Frontend Developer to lead our UI team...',
        'requirements': '- 5+ years React experience\n- Strong CSS/Tailwind skills\n- Experience with Next.js'
    },
    {
        'title': 'Product Designer (UI/UX)',
        'company_name': 'Creative Studio',
        'location': 'New York, NY',
        'salary_range': '$90k - $130k',
        'job_type': 'Full Time',
        'description': 'Join our creative team to build beautiful, user-centric interfaces...',
        'requirements': '- Figma mastery\n- Portfolio demonstrating web apps\n- UX research capability'
    },
    {
        'title': 'Backend Developer (Python/Django)',
        'company_name': 'DataSystems Inc',
        'location': 'Austin, TX / Hybrid',
        'salary_range': '$110k - $150k',
        'job_type': 'Full Time',
        'description': 'Looking for a Django expert to scale our core API services.',
        'requirements': '- 3+ years Django experience\n- REST API design\n- PostgreSQL performance tuning'
    }
]

for job_data in mock_jobs:
    job, created = Job.objects.get_or_create(
        title=job_data['title'],
        recruiter=recruiter,
        defaults={
            'company_name': job_data['company_name'],
            'location': job_data['location'],
            'salary_range': job_data['salary_range'],
            'job_type': job_data['job_type'],
            'description': job_data['description'],
            'requirements': job_data['requirements']
        }
    )
    if created:
        print(f"Created job: {job.title}")

print("Mock jobs setup complete.")
