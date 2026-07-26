Notes pour faire la documentation plus tard

-> utilisation de Flask car c'est ce qu'on a vu en cours pour Python - évite le changement brutal
-> au début implémentation de Werkzeug qui prend en compte les requêtes HTTP entrantes pour en faire un objet python 'request'
utilisable dans le code. Et fourni le serveur de dev 'flask run'
Werkzeug == couche HTTP
-> Werkzeug sera à remplacer par GUNICORN par exemple en prod car il ne fait que du monothread donc n'a pas la capcité 
d'absorber un flux entrant de production

-> création de 'blueprints' pour les routes de l'app, ce qui permet de les appel
