Déploiement de production
=====================

Ce README fournit de la documentation pour aider à déployer Yaksh dans un environnement de production
environnement. Si vous souhaitez faire un essai avec Yaksh, voici un
`Guide de démarrage rapide <https://github.com/FOSSEE/online\_test/blob/master/README.rst>`__


requirements
=============

Python 3.6, 3.7, 3.8

Django 3.0.3


####################
Déploiement local
####################

Suivez ces étapes pour déployer localement sur le serveur. Pour obtenir des instructions de déploiement à l'aide de Docker, consultez `Déploiement de plusieurs Dockers <https://github.com/FOSSEE/online_test/blob/add-docker-compose-test/README_production.rst#deploying-multiple-dockers>`__

Prérequis
^^^^^^^^^^^^^

1. Assurez-vous que `pip <https://pip.pypa.io/en/latest/installing.html>`__ est
   installée

2. Installez le serveur MySQL

3. Installez les dépendances du système Python MySQL

4. Installez Apache Server pour le déploiement

5. Créez une base de données nommée ``yaksh`` en suivant les étapes ci-dessous

   ::

      $> mysql -u root -p
      $> mysql> create database yaksh

6.Ajouter un utilisateur nommé ``yaksh_user`` et lui donner accès sur la base de données
   ``yaksh`` en suivant les étapes ci-dessous

   ::

      mysql> grant usage on yaksh to yaksh_user@localhost identified
      by 'mysecretpassword';

      mysql> grant all privileges on yaksh to yaksh_user@localhost;


Installation et utilisation
^^^^^^^^^^^^^^^^^^^^

Pour installer cette application, suivez les étapes ci-dessous :

1. Clonez ce référentiel et cd vers le référentiel cloné.

   ::

      git clone  https://github.com/FOSSEE/online_test.git

   ::

      cd online_test

2. Installer les dépendances Yaksh, Exécuter

   ::

      pip3 install -r requirements/requirements-common.txt

   ::

      pip3 install -r requirements/requirements-production.txt

   ::

      sudo pip3 install -r requirements/requirements-codeserver.txt


3. Renommez le ``.sampleenv`` en ``.env``

4. Dans le fichier ``.env``, décommentez ce qui suit et remplacez les valeurs
(veuillez conserver les paramètres restants tels quels);

   ::

      DB_ENGINE=mysql # Or psycopg (postgresql), sqlite3 (SQLite)
      DB_NAME=yaksh
      DB_USER=root
      DB_PASSWORD=mypassword # Or the password used while creating a Database
      DB_PORT=3306

5. Run:

   ::

        $ python manage.py migrate

6. Exécutez le serveur python fourni. Cela garantit que le code est
   exécuté dans un environnement sûr. Faites ceci comme ceci :

   ::

        $ sudo python3 -m yaksh.code_server # Pour Python 3.x

    Mettez cela en arrière-plan une fois qu'il a commencé car cela ne sera pas
    renvoyer l'invite. Il est important que le serveur fonctionne
    *avant* que les étudiants commencent à passer l'examen. L'utilisation de sudo est nécessaire
    puisque le serveur est exécuté en tant qu'utilisateur "nobody". Le serveur de code nécessite plusieurs
    paramètres spécifiés dans le fichier `.env` tels que "N\_CODE\_SERVERS",
    "SERVER\_TIMEOUT", "SERVER\_POOL\_PORT", "SERVER\_HOST\_NAME"
    mis à certaines valeurs par défaut.

    Ces paramètres peuvent être modifiés en différentes valeurs en fonction de votre
    exigence. Plusieurs processus de serveur de code sont générés en fonction de
    Valeur "N\_CODE\_SERVERS".
    Le "SERVER\_TIMEOUT" peut également être modifié. C'est le temps maximum autorisé
    pour exécuter le code soumis.

    Vous pouvez également utiliser un serveur de code Dockerisé,
    voir :ref:`Dockerized Code Server <https://github.com/FOSSEE/online_test/blob/add-docker-compose-test/README_production.rst#using-dockerized-code-server>`__


7.  Le script ``wsgi.py`` devrait faciliter son déploiement en utilisant
    mod\_wsgi. Vous devrez ajouter une ligne de la forme :

    ::

        WSGIScriptAlias / "/online_test/wsgi.py"

    à votre apache.conf. Pour plus de détails, consultez la documentation de Django ici :

    https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/

8. Créer un Superuser/Administrator:

   ::

        python manage.py createsuperuser

9. Accédez à http://desired\_host\_or\_ip:desired\_port/exam

   Et vous devriez être prêt.

10. Notez que le répertoire "output" présent dans le dossier "yaksh_data" sera
    contiennent des répertoires, un pour chaque utilisateur.
    Les fichiers de code des utilisateurs sont créés dans le répertoire "output" qui peut être utilisé pour
    vérifier plus tard.

11. En tant qu'utilisateur administrateur, vous pouvez visiter http://desired\_host\_or\_ip/exam/monitor pour
    afficher les résultats et les données utilisateur de manière interactive. Vous pouvez également « noter » les papiers
    manuellement si nécessaire.

.. _dockerized-code-server :

Utilisation du serveur de code dockerisé
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Installer
   `Docker <https://docs.docker.com/engine/installation/>`__

2. Allez dans le répertoire où se trouve le projet

   ::

        cd /chemin/vers/online_test

3. Créez une image fixe. Cela peut prendre quelques minutes,

   ::

        docker build -t yaksh_code_server -f ./docker/Dockerfile_codeserver

4. Vérifiez si l'image a été créée à l'aide de la sortie de ``docker
   images``

5. Exécutez le script d'appel à l'aide de la commande ``invoke start``. La commande
   va créer et exécuter un nouveau conteneur Docker (qui exécute le
   code\_server.py à l'intérieur), il liera également les ports de l'hôte
   avec ceux du conteneur

6. Vous pouvez utiliser ``invoke --list`` pour obtenir une liste de toutes les commandes disponibles


.. _deploying-multiple-dockers :

########################################
Déployer plusieurs Dockers
########################################

Suivez ces étapes pour déployer et exécuter le serveur Django, l'instance MySQL et
Code Server dans des instances Docker distinctes.

1. Installez `Docker <https://docs.docker.com/engine/installation/>`__

2. Installez `Docker Compose <https://docs.docker.com/compose/install/>`__

3. Renommez le ``.sampleenv`` en ``.env``

4. Dans le fichier ``.env``, décommentez toutes les valeurs et conservez les valeurs par défaut
   comme si.

5. Allez dans le répertoire ``docker`` où se trouve le projet :
   
   ::

        cd /chemin/vers/online_test/docker

6. Construisez les images Docker

   ::

        invoke build

7. Exécutez les conteneurs et les scripts nécessaires pour déployer le Web
   application

   ::

        invoke begin

8. Assurez-vous que tous les conteneurs sont ``Up`` et stables

   ::

        invoke status

8. Exécutez les conteneurs et les scripts nécessaires pour déployer le Web
   application, ``--fixtures`` vous permet de charger des appareils.

   ::

        invoke deploy --fixtures

10. Pour arrêter les conteneurs, exécutez

   ::

        invoquer halt

11. Vous pouvez utiliser ``invoke restart`` pour redémarrer les conteneurs sans
    les supprimer.

12. Retirez les conteneurs

   ::

        invoquer remove

13. Vous pouvez utiliser ``invoke --list`` pour obtenir une liste de toutes les commandes disponibles.