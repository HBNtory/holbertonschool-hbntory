Notes pour faire la documentation plus tard

-> utilisation de Flask car c'est ce qu'on a vu en cours pour Python - évite le changement brutal
-> au début implémentation de Werkzeug qui prend en compte les requêtes HTTP entrantes pour en faire un objet python 'request'
utilisable dans le code. Et fourni le serveur de dev 'flask run'
Werkzeug == couche HTTP
-> Werkzeug sera à remplacer par GUNICORN par exemple en prod car il ne fait que du monothread donc n'a pas la capcité 
d'absorber un flux entrant de production

-> création de 'blueprints' pour les routes de l'app, ce qui permet de les appel
    -> l'idée d'un blueprint est un support de route intermédiaire qui permet d'éviter les long fichiers interminables 
        ou les erreurs d'imports circulaires.

-> le fait de donner la variable `__name__` à Flask en argument permet de laisser Flask se situer et aussi de chercher 
automatiquement les dossiers `templates/` et `static/`

-> le `__name__` revient aussi en arguement dans les blueprints pour la même raison. 

-> pour le binding de ports j'ai choisi le 8080 car sur le mac mon port 5000 était déjà prit. 
    -> si jamais pour plus tard la possibilité de prendre des ports classiques : 8888 ou 3000 tout les ports libre au
        dessus de 1024 (ports priviligiés "well-known")
    -> possiblité de mettre les ports dans les variables d'environement
        ```yaml
            ports:
                -"8080:5000"
#                   |   |
#                   |   └─port DANS le conteneur (celui que Flask écoute)
#                   └─port SUR ma machine (celui sur laquelle on va taper dans le navigateur)
        ```

-> pour le fichier de config il sera utilisé afin d'avoir accès à toutes les variables d'env nécessaires récupérées dans 
le .env via os. 
    -> avec la ligne `app.config.from_object(Config)` Flask va parcourt les attributs la class Config (en majuscule) et les 
copie dans app.config comme ça on peut les lire partout dans l'app grâce à `app.config["SECRET_KEY"]` par exemple.