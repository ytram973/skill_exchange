from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("skills/", views.SkillListView.as_view(), name="skill_list"),
    path("my-skills/", views.MySkillsView.as_view(), name="my_skills"),
    path("help-request/create/", views.HelpRequestCreateView.as_view(), name="help_request_create"),
    path("help-request/list/", views.HelpRequestListView.as_view(), name="help_request_list"),
    path("help-request/<int:pk>/offer/", views.MakeOfferView.as_view(), name="make_offer"),  
]