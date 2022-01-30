Guide pour la version test :
======================
   A suivre avant chaque sortie.

1. Installation et déploiement :
   ----------------------------
   a. Suivez le guide d'instructions pour voir si toutes les étapes fonctionnent sans problème.

   b. Essayez de vous connecter avec l'administrateur, l'étudiant, l'enseignant individuellement.

   c. Essayez d'exécuter `rm -rf ../*` à partir de l'interface de quiz pour que bash vérifie si l'étudiant n'est personne
      docker à l'intérieur.

   d. Essayez d'exécuter `rm -rf ../*` depuis l'interface de quiz pour bash avec `invoke start --unsafe`
      pour vérifier si l'étudiant n'est pas personne.


2. Authentification :
   ---------------
   a. **Inscription sur Yaksh :**
      - Sur la page de destination, cliquez sur le bouton d'inscription.
      - Sur le formulaire d'inscription de l'utilisateur, essayez de vous inscrire avec un champ vide. Cela devrait rediriger vers la même page avec le champ de notification nécessaire.
      - Essayez la même chose avec tous les champs remplis. Cela devrait vous inscrire et rediriger vers la page des quiz.

   b. **Connectez-vous avec Google/Facebook oauth :**
         (À faire à partir du serveur live uniquement)
   - Vérifiez si l'authentification google facebook oauth fonctionne ou non.

   c. **Mot de passe oublié:**
   - Cliquez sur le bouton Mot de passe oublié.
   - Entrez une adresse e-mail valide et cliquez sur réinitialiser.
   - Vérifiez le courrier, cliquez sur le lien et changez le mot de passe.
   - Vérifiez si le nouveau mot de passe est valide.

   d. **Changer le mot de passe**
      - Connectez-vous séparément en tant qu'étudiant et en tant que modérateur et cliquez sur modifier le mot de passe.
      - Essayez de changer le mot de passe et vérifiez si le mot de passe est modifié.

   e. **Editer le profil**
      - Essayez de modifier le profil et vérifiez si les données sont correctement mises à jour.
3. Interface étudiant.
   ------------------

   a. Recherchez un cours à l'aide du code du cours.

   b. Essayez d'essayer Demo Quiz.

   c. Dans le quiz, essayez tous les types de questions. Essayez d'essayer les mêmes questions avec la bonne réponse
      puis mauvaise réponse et vice versa.

   d. Essayez de quitter le quiz entre les deux avec quelques questions restantes et revenez à
      l'interface en cliquant sur non pour vérifier s'il revient en toute sécurité au quiz.

   e. Essayez de quitter le quiz entre les deux, avec quelques questions restantes et quittez le quiz en
      en cliquant sur oui pour vérifier s'il quitte le quiz en toute sécurité.

   F. Essayez de fermer le navigateur entre le quiz et redémarrez le quiz pour vérifier si le quiz
      reprend correctement.

   g. Essayez de vous déplacer d'avant en arrière à l'aide du bouton de retour du navigateur pour vérifier si plusieurs objets
      erreur se produit.

   h. Essayez toutes les questions et vérifiez si la révision des questions fonctionne.

   i. Essayez toutes les questions et essayez de quitter et cliquez sur non et revenez à l'interface.

   j. Essayez toutes les questions et essayez de quitter et cliquez sur oui et quittez le quiz.

   k. Essayez les étapes c à g pour une seule question dans un quiz.

   l. Essayez de répondre aux questions jusqu'à ce que le temps soit écoulé et vérifiez si le délai d'attente ferme le quiz
      sans encombre.

   m. Essayez de voir le papier-réponse si l'élève obtient les bonnes notes.

4. Interface du modérateur.
   --------------------

   a. Essayez de cliquer sur le lien du quiz du tableau de bord du modérateur pour vérifier s'il redirige correctement vers
      surveiller la page pour ce quiz.

   b. Cliquez sur créer un cours de démonstration et vérifiez si le cours et les quiz sont créés.

   c. **Moniteur**
      - Cliquez sur le lien de téléchargement csv et vérifiez si les données utilisateur sont correctement enregistrées.
      - Cliquez sur le lien du nom de l'étudiant et vérifiez si les réponses des utilisateurs sont soumises correctement,
         les marques sont mises à jour correctement.
      - Cliquez sur les statistiques de la question pour vérifier que les statistiques appropriées sont affichées.

   d. **Utilisateur Grade**
      - Cliquez sur le lien du quiz, puis sur le lien du nom de l'étudiant et cochez
         si les réponses des utilisateurs s'affichent correctement.
      - Essayez de mettre à jour les notes et d'ajouter des commentaires pour un étudiant.
      - Cochez les notes pour chaque question et les notes totales pour vous assurer que les notes sont correctement mises à jour.
      - Pour les questions non codées, assurez-vous que la dernière tentative est notée.
      - Essayez de vérifier plusieurs tentatives pour un utilisateur.
      - Vérifiez les notes de classement partielles pour une question.
      - Essayez de télécharger des devoirs par quiz et par utilisateur.

   e. **Cours**
      - Essayez d'inscrire/rejeter quelques étudiants pour un cours.
      - Créez des quiz pour un cours.
      - Essayez d'ajouter des enseignants au cours.
      - Téléchargez le cours csv pour obtenir la liste des étudiants inscrits et les notes du quiz.
      - Vérifiez si les enseignants ont tous les privilèges dont dispose un modérateur pour un cours.
      - Définir l'heure d'inscription à un cours et vérifier si les étudiants ne sont pas inscrits après la
         heure de fin.

   F. **Reclasser**
      - Essayez de reclasser les papiers par utilisateur, par question et par quiz

   g. **Des questions**
      - Essayez de créer des questions.
      - Essayez de télécharger des questions.
      - Essayez de télécharger des questions.
      - Essayez de filtrer les questions à l'aide de filtres et de balises.
      - Sélectionnez quelques questions et testez les questions sélectionnées.

   h. **Quiz**
      - Essayez d'essayer le mode utilisateur et le mode dieu pour un quiz.
      - Essayez de changer l'état actif, l'heure de début, l'heure de fin et tentez le quiz.

   i. **Questionnaire**
      - Ajoutez des questions fixes, des questions aléatoires dans un questionnaire et tentez le quiz.
      - Activez la lecture aléatoire automatique et essayez de tenter le quiz.
