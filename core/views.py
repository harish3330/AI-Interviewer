from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Interview, InterviewSession

from .models import Profile, Interview, InterviewSession
from .ai import generate_interview_questions



def home(request):
    return render(request, 'core/home.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={'role': 'CANDIDATE'}
            )

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})



@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'CANDIDATE'}
    )

    if profile.role == 'HR':
        return redirect('hr_dashboard')
    return redirect('candidate_dashboard')



@login_required
def hr_dashboard(request):
    interviews = Interview.objects.filter(created_by=request.user)
    return render(request, 'core/hr_dashboard.html', {
        'interviews': interviews
    })



@login_required
def hr_interviews(request):
    interviews = Interview.objects.filter(created_by=request.user)
    return render(request, 'core/hr_interviews.html', {
        'interviews': interviews
    })



@login_required
def hr_applications(request):
    sessions = InterviewSession.objects.select_related(
        'candidate', 'interview'
    ).order_by('-applied_at')

    return render(request, 'core/hr_applications.html', {
        'sessions': sessions
    })


@login_required
def update_application_status(request, session_id, status):
    session = get_object_or_404(InterviewSession, id=session_id)
    session.status = status
    session.save()
    return redirect('hr_applications')



@login_required
def create_interview(request):
    if request.method == 'POST':
        Interview.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            skills=request.POST.get('skills'),
            roles_responsibilities=request.POST.get('roles'),
            evaluation_criteria=request.POST.get('criteria'),
            created_by=request.user
        )
        return redirect('hr_interviews')

    return render(request, 'core/create_interview.html')




@login_required
def candidate_dashboard(request):
    interviews = Interview.objects.all()
    sessions = InterviewSession.objects.filter(candidate=request.user)

    return render(request, 'core/candidate_dashboard.html', {
        'interviews': interviews,
        'sessions': sessions
    })



@login_required
def start_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)

    session, created = InterviewSession.objects.get_or_create(
        interview=interview,
        candidate=request.user
    )

    if request.method == 'POST':
        answers = request.POST.get('answers')

        session.answers = json.loads(answers)
        session.status = 'PENDING'

        
        session.score = len(session.answers) * 10

        session.save()

        return redirect('candidate_dashboard')

    questions = generate_interview_questions(
        topic=interview.title,
        skills=interview.skills,
        level="Beginner"
    )

    return render(request, 'core/start_interview.html', {
        'interview': interview,
        'questions': questions,
        'session': session
    })



