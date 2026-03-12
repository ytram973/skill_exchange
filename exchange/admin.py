from django.contrib import admin
from .models import Skill, UserSkill, HelpRequest, HelpOffer


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Administration des compétences.
    Permet de rechercher une compétence par son nom.
    """
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    """
    Administration des compétences des utilisateurs.
    Permet de filtrer par compétence.
    """
    list_display = ("user", "skill")
    list_filter = ("skill",)


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    """
    Administration des demandes d'aide.
    Permet de filtrer par statut et par compétence,
    et de rechercher par description d'activité.
    """
    list_display = ("requester", "skill_needed", "date", "is_taken")
    list_filter = ("is_taken", "skill_needed")
    search_fields = ("activity_description",)


@admin.register(HelpOffer)
class HelpOfferAdmin(admin.ModelAdmin):
    """
    Administration des offres d'aide.
    Affiche l'utilisateur qui aide, la demande concernée et la date de création.
    """
    list_display = ("helper", "help_request", "created_at")