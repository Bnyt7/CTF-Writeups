# Sandwich
Web - medium
(2 solves)


On peut s'inscrire au site avec un nom, prénom, email. 
Quand on se connecte avec notre nouveau compte, on a accès à un chat, il y a une conversation avec différents personnes dont un admin.
Il y a aussi une messagerie fictive où on peut recevoir des mails en bas à droite.

Il y a aussi une page "mot de passe oublié" qui permet de réinitialiser son mot de passe.
Si on met notre mail et qu'on se reconnecte de nouveau, on peut obtenir un lien de réinitialisation du mot de passe dans la fausse messagerie.

Dans le lien, le token utilisé est sous la forme d'UUIDv1. Ce dernier est généré en fonction d'une adresse MAC et d'un timestamp correspondant au nombre de dixièmes de micro-secondes écoulées depuis le 15 Octobre 1582 à minuit (UTC).
Si on sait exactement quand l'uuid a été généré, on peut alors le retrouver.

Il est possible d'envoyer des messages dans la discussion, cela passe par une api. Dans la réponse de l'api, on peut récupérer des informations intéressantes comme le nom du mail de l'admin :
``admin@boulangerie.fr``


Le but est donc de réinitaliser le mot de passe de l'admin, retrouver l'uuid utilisé et changer le mot de passe.


On peut essayer de retrouver le token généré en envoyant 3 requêtes à la suite dans la page mdp oublié.

- notre mail
- Le mail de l'admin
- notre mail

C'est ce qui est appelé un "sandwich attack"

On peut utiliser un proxy pour envoyer les trois requêtes à la suite avec un minimum de délai.

Dans la boîte de réception de notre compte, on obtient nos deux liens. 

Le lien pour reset le mot de passe de l'admin a un uuid dont le timestamp se situe entre les deux, on teste alors toutes les possibilités jusqu'à avoir le bon lien, reset le mot de passe de l'admin et se connecter avec.

Flag : ``CYBN{1_pR3f3r_cH3e53_S4ndWIcH_Th4N_Uu1D_S4nDW1Ch``



Ressources : 
- https://medium.com/@iason.tzortzis/why-uuidv1-should-not-be-used-to-generate-security-tokens-explained-22f8867ea695
- https://www.xmco.fr/actualite-veille-cybersecurite-fr/exploitation-uuid-compromission-compte/


