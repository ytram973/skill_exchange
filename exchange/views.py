from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, FormView
from .models import Skill, UserSkill, HelpRequest, HelpOffer


class HomeView(ListView):
    """
    Page d'accueil accessible à tous les visiteurs.
    Affiche la liste des créneaux d'aide acceptés de façon anonyme.
    """
    
    model = HelpOffer
    template_name = 'exchange/home.html'
    context_object_name = 'offers'
    
    def get_queryset(self):
        """Retourne les offres d'aide triées par date de création décroissante."""
        return HelpOffer.objects.select_related('help_request__requester', 'help_request__skill_needed').order_by('-created_at')
    



class SkillListView(ListView):
    """
    Affiche la liste de toutes les compétences disponibles sur la plateforme.
    Accessible à tous les visiteurs.
    """
    model = Skill
    template_name = "exchange/skill_list.html"
    context_object_name = "skills"



class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Tableau de bord de l'utilisateur connecté.
    Affiche ses demandes d'aide et ses offres d'aide.
    """
    template_name = "exchange/dashboard.html"

    def get_context_data(self, **kwargs):
        """Ajoute les demandes et offres de l'utilisateur au contexte."""
        ctx = super().get_context_data(**kwargs)
        ctx["my_requests"] = HelpRequest.objects.filter(requester=self.request.user).order_by("date")
        ctx["my_offers"] = HelpOffer.objects.filter(helper=self.request.user).order_by("created_at")
        return ctx


class MySkillsView(LoginRequiredMixin, TemplateView):
    """
    Permet à l'utilisateur connecté de gérer ses compétences.
    Il peut ajouter ou retirer une compétence depuis la liste disponible.
    """
    template_name = "exchange/my_skills.html"

    def get_context_data(self, **kwargs):
        """
        Retourne deux listes :
        - owned : compétences que l'utilisateur possède
        - available : compétences qu'il ne possède pas encore
        """
        ctx = super().get_context_data(**kwargs)
        my_skill_ids = UserSkill.objects.filter(user=self.request.user).values_list("skill_id", flat=True)
        ctx["owned"] = Skill.objects.filter(id__in=my_skill_ids)
        ctx["available"] = Skill.objects.exclude(id__in=my_skill_ids)
        return ctx

    def post(self, request, *args, **kwargs):
        """Ajoute ou retire une compétence selon l'action envoyée par le formulaire."""
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


class HelpRequestCreateView(LoginRequiredMixin, TemplateView):
    """
    Permet à l'utilisateur connecté de créer une demande d'aide.
    Seules les compétences qu'il ne possède pas sont proposées.
    """
    template_name = "exchange/help_request_create.html"

    def get_context_data(self, **kwargs):
        """Retourne les compétences que l'utilisateur ne possède pas."""
        ctx = super().get_context_data(**kwargs)
        my_skill_ids = UserSkill.objects.filter(user=self.request.user).values_list("skill_id", flat=True)
        ctx["skills"] = Skill.objects.exclude(id__in=my_skill_ids)
        return ctx

    def post(self, request, *args, **kwargs):
        """Crée la demande d'aide et redirige vers le tableau de bord."""
        skill = get_object_or_404(Skill, id=request.POST.get("skill_id"))
        HelpRequest.objects.create(requester=request.user,skill_needed=skill,activity_description=request.POST.get("description"),
            date=request.POST.get("date"),
        )
        messages.success(request, "Demande créée avec succès.")
        return redirect("dashboard")


class HelpRequestListView(LoginRequiredMixin, ListView):
    """
    Affiche les demandes d'aide disponibles qui correspondent
    aux compétences de l'utilisateur connecté.
    Exclut ses propres demandes et les demandes déjà prises en charge.
    """
    template_name = "exchange/help_request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        """Retourne les demandes filtrées par compétences de l'utilisateur."""
        my_skill_ids = UserSkill.objects.filter(user=self.request.user).values_list("skill_id", flat=True)
        return HelpRequest.objects.filter(skill_needed__in=my_skill_ids,is_taken=False,
        ).exclude(requester=self.request.user).order_by("date")


class MakeOfferView(LoginRequiredMixin, TemplateView):
    """
    Permet à l'utilisateur connecté de proposer son aide
    en réponse à une demande d'aide.
    Une fois l'offre créée, la demande est marquée comme prise en charge.
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Crée une offre d'aide pour la demande correspondante.
        Redirige vers le tableau de bord si l'opération réussit.
        """
        help_request = get_object_or_404(HelpRequest, pk=pk, is_taken=False)

        if help_request.requester == request.user:
            messages.error(request, "Vous ne pouvez pas répondre à votre propre demande.")
            return redirect("help_request_list")

        HelpOffer.objects.create(helper=request.user, help_request=help_request)
        help_request.is_taken = True
        help_request.save()
        messages.success(request, "Votre offre a été enregistrée !")
        return redirect("dashboard")