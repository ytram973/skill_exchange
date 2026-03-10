from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE ,related_name='users')
    class Meta:
        unique_together = ('user', 'skill')
            
    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"

class HelpRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_requests")
    skill_needed = models.ForeignKey(Skill, on_delete=models.CASCADE)
    activity_description = models.TextField()
    date = models.DateField()
    is_taken = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} – {self.skill_needed.name} – {self.date}"


class HelpOffer(models.Model):
    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_offers")
    help_request = models.OneToOneField(HelpRequest, on_delete=models.CASCADE, related_name="offer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.helper.username} → {self.help_request}"