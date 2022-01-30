Yaksh
=====

|État de la construction| |État de la documentation| |État de la version| |État de la couverture|

Pour obtenir un aperçu de l'interface Yaksh, veuillez vous référer à la documentation utilisateur sur `Yaksh Docs <http://yaksh.readthedocs.io>`_


Ceci est un guide de démarrage rapide pour aider les utilisateurs à configurer une instance d'essai. Si vous souhaitez déployer Yaksh dans un environnement de production, voici un `Guide de déploiement de production <https://github.com/FOSSEE/online\_test/blob/master/README\_production.rst>`_

introduction
=============

Ce projet fournit une application « examen » qui permet aux utilisateurs de passer un examen en ligne
quiz de programmation.

Caractéristiques
========

- Définir des problèmes de programmation assez compliqués et faire résoudre par les utilisateurs
   le problème.
- Vérification immédiate de la solution de code.
- Prend en charge à peu près les questions de codage arbitraires en Python, C, C++, Java, R, Scilab et
   Frapper.
- Prend en charge les choix multiples, remplissez les blancs, organisez les options et les questions basées sur le téléchargement de fichiers.
- Puisqu'il fonctionne sur Python, vous pouvez techniquement tester n'importe quel Python
   bibliothèque basée.
- Créer un cours avec des leçons et des quiz pour l'apprentissage en ligne.
- Surveillance presque en temps réel pour le quiz.
- Prend en charge la notation automatique et manuelle, le reclassement du quiz.
- Ajouter un système de notation au cours.
- S'adapte à plus de 500+ utilisateurs simultanés.
- Distribué sous licence BSD.

Pour avoir un aperçu de toutes les fonctionnalités disponibles, consultez notre site Web de démonstration https://yaksh-demo.fossee.in. Il dispose de 50 connexions d'enseignants et d'étudiants.

**Sample teacher login**

Username: teacher
Password: teacher

**Sample student login**

Username: student
Password: student

Requirements
============

Python 3.6, 3.7, 3.8

Django 3.0.3

Celery 4.4.2

Installation
============

**Remarque** : Actuellement, seuls Linux et MacOS sont pris en charge pour le projet.

Si Python 3.6 et supérieur n'est pas disponible dans le système, nous vous recommandons d'utiliser
miniconda. Téléchargez miniconda avec Python 3.6 et supérieur.

**Installation de Miniconda**

1. Téléchargez miniconda depuis https://docs.conda.io/en/latest/miniconda.html selon la version du système d'exploitation.

2. Suivez les instructions d'installation comme indiqué dans https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation

3. Redémarrez le terminal.

**Prérequis**

* **Installer le serveur redis**

  Redis est requis pour celery. Celery exécute une tâche en arrière-plan pour réévaluer les soumissions.

  ::

      sudo apt install redis-server (Debian/Ubuntu)

      yum install redis (Centos)

* **Démarrer le serveur redis**

  ::
     
      systemctl start redis
* **Vérifier l'état du serveur redis**

  ::

      systemctl status redis

* **Lancer  celery worker**
  
  ::

      celery -A online_test worker -B

* Assurez-vous que `pip <https://pip.pypa.io/en/latest/installing.html>`_ est installé

**Installation de Yaksh**

* **Cloner le reporsitory**

  ::

      git clone https://github.com/FOSSEE/online_test.git

* **Allez dans le répertoire online_test**

  ::

      cd online_test

* **Installez les dépendances** :

  * Installer Django et ses dépendances

    ::

        pip3 install -r requirements/requirements-common.txt

  * Installer les dépendances du serveur de code

    ::

        sudo pip3 install -r requirements/requirements-codeserver.txt


Démarrage rapide
^^^^^^^^^^^

1. Démarrez le serveur de code qui exécute le code utilisateur en toute sécurité :

   - Pour exécuter le serveur de code dans un environnement docker en bac à sable, exécutez le
      commander:

      ::

          $ invoke start

   - Assurez-vous que Docker est installé sur votre système
      préalablement. `Docker
      Installation <https://docs.docker.com/engine/installation/#desktop>`__

   - Pour exécuter le serveur de code sans docker, utilisez localement :

      ::

          $ invoke start --unsafe

   - Notez que cette commande exécutera le serveur de code yaksh localement sur votre
      machine et est sensible au code malveillant. Tu vas devoir
      installer les exigences du serveur de code en mode sudo.

2. Sur un autre terminal, lancez l'application à l'aide de la commande suivante :

   ::

       $ invoke serve

   - *Remarque :* La commande serve exécutera le serveur d'applications Django
      sur le port 8000 et donc ce port sera indisponible pour d'autres
      processus.

3. Ouvrez votre navigateur et ouvrez l'URL ``http://localhost:8000/exam``

4. Connectez-vous en tant qu'enseignant pour modifier le quiz ou en tant qu'étudiant pour répondre au quiz
   Crédits:

   - Étudiant - Nom d'utilisateur : student \| Mot de passe : student
   - Enseignant - Nom d'utilisateur : teacher \| Mot de passe : teacher

5. L'utilisateur peut également se connecter à l'administrateur par défaut de Django en utilisant ;

   - Admin - Nom d'utilisateur : admin \| Mot de passe : admin

Historique
=======

Chez FOSSEE, Nishanth avait mis en place une belle application basée sur Django pour tester
Questions à choix multiple. Prabhu Ramachandran s'est inspiré d'un
concours de programmation qu'il a vu à PyCon APAC 2011. Chris Boesch, qui
administré le concours, utilisé une belle application web
`Singpath <http://singpath.com>`__ qu'il avait construit sur GAE qui
essentiellement vérifié votre code Python, en direct. Cela l'a rendu amusant et
intéressant.

Prabhu voulait une implémentation qui n'était pas liée à GAE et a donc écrit
la coupe initiale de ce qui est maintenant 'Yaksh'. L'idée étant que n'importe qui peut
utilisez-le pour tester les compétences de programmation des étudiants et ne pas avoir à vous soucier de
notant leurs réponses manuellement et le font à la place sur leurs machines.

L'application a depuis été refactorisée et maintenue par FOSSEE
Développeurs.

Contact
=======

Pour plus d'informations et d'assistance, vous pouvez contacter

Équipe Python de FOSSEE : pythonsupport@fossee.in

Licence
=======

Celui-ci est distribué selon les termes de la licence BSD. droits d'auteur
l'information est au bas de ce fichier.

Auteurs
=======

`Développeurs FOSSEE <https://github.com/FOSSEE/online_test/graphs/contributors>`_

Copyright (c) 2011-2017 `FOSSEE <https://fossee.in>`_


.. |État de la construction| image :: https://travis-ci.org/FOSSEE/online_test.svg?branch=master
   :cible: https://travis-ci.org/FOSSEE/online_test
.. |État de la documentation| image :: https://readthedocs.org/projects/yaksh/badge/?version=latest
   :cible: http://yaksh.readthedocs.io/en/latest/?badge=latest
.. |État de la version| image :: https://badge.fury.io/gh/fossee%2Fonline_test.svg
    :cible: https://badge.fury.io/gh/fossee%2Fonline_test
.. |État de la couverture| image :: https://codecov.io/gh/fossee/online_test/branch/master/graph/badge.svg
    :cible: https://codecov.io/gh/fossee/online_test
