## Utilisateur connecté

Toute personne ayant un compte et étant authentifiée.
*Hérite de tout ce que peut faire le visiteur, plus :*

### Permissions

1. **Se connecter / Se déconnecter**
    * Connexion via username + password
    * Déconnexion

2. **Gérer ses compétences**
    * Voir la liste des compétences qu'il possède
    * Ajouter une compétence depuis la liste globale
    * Retirer une compétence qu'il possède

3. **Créer une demande d'aide**
    * Choisir une compétence parmi celles qu'il ne possède pas
    * Décrire l'activité librement (champ texte)
    * Choisir une date (créneau = journée entière)
    * La demande est visible par les autres utilisateurs ayant la compétence correspondante

4. **Voir les demandes qui correspondent à ses skills**
    * Affiche les HelpRequest d'autres utilisateurs
    * Filtrées : uniquement celles dont la skill_needed fait partie de ses compétences
    * Exclues : ses propres demandes, les demandes déjà prises (is_taken = True)
    * Informations visibles : prénom, nom, email du demandeur, compétence, activité, date
    * Triées par date croissante

5. **Proposer son aide**
    * Depuis la liste précédente, l'utilisateur clique sur "Je propose mon aide"
    * Crée un HelpOffer liant les deux utilisateurs
    * La demande passe à is_taken = True et disparaît de toutes les listes
