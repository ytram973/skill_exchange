from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    """
    Représente une compétence disponible sur la plateforme.
    Les compétences sont créées par l'admin
    """

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        """Retourne le nom de la compétence."""
        return self.name


class UserSkill(models.Model):
    """
    Représente la relation entre un utilisateur et une compétence qu'il possède
    Un utilisateur ne peut pas avoir deux fois la même compétence
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='users')

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self) -> str:
        """Retourne le nom de l'utilisateur et la compétence associée."""
        return f"{self.user.username} - {self.skill.name}"


class HelpRequest(models.Model):
    """
    Représente une demande d'aide créée par un utilisateur.
    L'utilisateur indique la compétence recherchée, avec description
    de l'activité et une date.
    Le champ is_taken passe à True dès qu'une offre est acceptée.
    """

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_requests")
    skill_needed = models.ForeignKey(Skill, on_delete=models.CASCADE)
    activity_description = models.TextField()
    date = models.DateField()
    is_taken = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Retourne le demandeur, la compétence et la date de la demande."""
        return f"{self.requester.username} – {self.skill_needed.name} – {self.date}"


class HelpOffer(models.Model):
    """
    Représente une offre d'aide d'un utilisateur en réponse à une HelpRequest.
    Une demande ne peut recevoir qu'une seule offre.
    Une fois l'offre créée, les deux utilisateurs peuvent se contacter par email.
    """

    helper = models.ForeignKey(User, on_delete=models.CASCADE, related_name="help_offers")
    help_request = models.OneToOneField(HelpRequest, on_delete=models.CASCADE, related_name="offer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Retourne le nom de l'aidant et la demande concernée."""
        return f"{self.helper.username} → {self.help_request}"