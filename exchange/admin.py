from django.contrib import admin

# Register your models here.
from .models import Skill, UserSkill, HelpRequest, HelpOffer


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ("user", "skill")
    list_filter = ("skill",)


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "skill_needed", "date", "is_taken")
    list_filter = ("is_taken", "skill_needed")
    search_fields = ("activity_description",)


@admin.register(HelpOffer)
class HelpOfferAdmin(admin.ModelAdmin):
    list_display = ("helper", "help_request", "created_at")