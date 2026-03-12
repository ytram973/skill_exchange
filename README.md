# SkillSwap

Application web Django permettant l'échange de compétences entre utilisateurs.

## Présentation

SkillSwap permet à des personnes d'échanger leurs compétences (jardinage, informatique, cuisine...).
Un utilisateur peut proposer son aide sur une activité ou rechercher quelqu'un pour l'aider,
sur un créneau d'une journée entière.

## Stack technique

- Python 3.13
- Django 5.2
- SQLite
- HTML / CSS

## Installation
```bash
git clone https://github.com/ytram973/skill_exchange.git
cd skill-exchange
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Structure du projet
```
skill-exchange/
├── skillexchange/        ← configuration Django
│   ├── settings.py
│   └── urls.py
├── exchange/             ← application principale
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── exchange/
├── manage.py
└── requirements.txt
```

## Fonctionnalités

### Visiteur
- Voir les créneaux d'aide acceptés (affichage anonyme)
- Voir la liste des compétences disponibles

### Utilisateur connecté
- Gérer ses compétences (ajouter / retirer)
- Créer une demande d'aide avec une compétence, une description et une date
- Voir les demandes qui correspondent à ses compétences
- Proposer son aide sur une demande
- Contacter l'autre utilisateur par email une fois l'offre acceptée

## Modèles

- `Skill` — compétences disponibles, créées par l'admin
- `UserSkill` — compétences possédées par un utilisateur
- `HelpRequest` — demande d'aide d'un utilisateur
- `HelpOffer` — offre d'aide en réponse à une demande

## Auteur

Marty RABORD