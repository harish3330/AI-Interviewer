from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = (
        ('HR', 'HR'),
        ('CANDIDATE', 'Candidate'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CANDIDATE'
    )

    def __str__(self):
        return self.user.username


class Interview(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField()
    roles_responsibilities = models.TextField()
    evaluation_criteria = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ NEW

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    interview = models.ForeignKey('Interview', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.interview.title}"

