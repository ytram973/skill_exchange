from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, FormView
from .models import Skill, UserSkill, HelpRequest, HelpOffer


class HomeView(ListView):
    model = HelpOffer
    template_name = 'exchange/home.html'
    context_object_name = 'offers'
    
    def get_queryset(self):
        return HelpOffer.objects.select_related('help_request__requester', 'help_request__skill_needed').order_by('-created_at')
    



class SkillListView(ListView):
    model = Skill
    template_name = "exchange/skill_list.html"
    context_object_name = "skills"



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "exchange/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["my_requests"] = HelpRequest.objects.filter(requester=self.request.user).order_by("date")
        ctx["my_offers"] = HelpOffer.objects.filter(helper=self.request.user).order_by("created_at")
        return ctx


class MySkillsView(LoginRequiredMixin, TemplateView):
    template_name = "exchange/my_skills.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        my_skill_ids = UserSkill.objects.filter(user=self.request.user).values_list("skill_id", flat=True)
        ctx["owned"] = Skill.objects.filter(id__in=my_skill_ids)
        ctx["available"] = Skill.objects.exclude(id__in=my_skill_ids)
        return ctx

    def post(self, request, *args, **kwargs):
        skill_id = request.POST.get("skill_id")
        action = request.POST.get("action")
        skill = get_object_or_404(Skill, id=skill_id)

        if action == "add":
            UserSkill.objects.get_or_create(user=request.user, skill=skill)
            messages.success(request, f"Compétence « {skill.name} » ajoutée.")
        elif action == "remove":
            UserSkill.objects.filter(user=request.user, skill=skill).delete()
            messages.success(request, f"Compétence « {skill.name} » retirée.")
        return redirect("my_skills")


