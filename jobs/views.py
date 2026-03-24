from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def home(request):
    jobs = Job.objects.all().order_by('-created_at')
    
    # Optional search filtering
    q = request.GET.get('q', '')
    if q:
        jobs = jobs.filter(title__icontains=q) | jobs.filter(company_name__icontains=q)
        
    return render(request, 'jobs/home.html', {'jobs': jobs, 'query': q})

def about(request):
    return render(request, 'jobs/about.html')

@login_required
def create_job(request):
    if not request.user.is_recruiter:
        raise PermissionDenied("Only recruiters can post jobs.")
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated and request.user.is_seeker:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def apply_job(request, pk):
    if not request.user.is_seeker:
        raise PermissionDenied("Only job seekers can apply for jobs.")
    
    job = get_object_or_404(Job, pk=pk)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('jobs:job_detail', pk=job.pk)
        
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('jobs:dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def dashboard(request):
    if request.user.is_seeker:
        applications = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
        stats = {
            'total': applications.count(),
            'pending': applications.filter(status='Pending').count(),
            'shortlisted': applications.filter(status='Shortlisted').count(),
            'hired': applications.filter(status='Hired').count(),
        }
        return render(request, 'jobs/seeker_dashboard.html', {'applications': applications, 'stats': stats})
    elif request.user.is_recruiter:
        jobs = Job.objects.filter(recruiter=request.user).prefetch_related('applications').order_by('-created_at')
        total_applicants = sum(job.applications.count() for job in jobs)
        return render(request, 'jobs/recruiter_dashboard.html', {'jobs': jobs, 'total_applicants': total_applicants})
    return redirect('jobs:home')
