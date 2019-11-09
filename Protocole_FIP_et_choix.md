Le protocole FIP est un protocole de gestion de bus basé sur le modèle producteur/consommateur.  
Différents objets et messages peuvent être échangés, des producteurs vers les consommateurs.  
Les échanges sont gérées par un *arbitre de bus* qui est chargé d'initier les échanges. Les objets transférés peuvent être périodiques ou pas. Étant donné notre sujet, il semblerait qu'**on ne doive gérer que les objets périodiques**.  

Les objets sont diffusés en broadcast, tandis que les messages sont envoyés en pair-à-pair. Vu le cours, **nous n'allons utiliser uniquement que la transmission d'objets**.  
Les objets sont identifiés grâce à un ID. Chaque producteur/consommateur est lié à un plusieurs objets identifiés. L'arbitre de bus est chargé de déterminer en fonction de tous les objets périodiques, un ordonnencement des tâches --- c'est à dire quels objets sont envoyés à quelle période. Il construit pour cela une table. Dans notre cas, **nous n'avons il semblerait qu'un seul type d'objet, et uniquement un producteur et un consommateur**, donc je pense qu'il n'est pas nécessaire de créer cette table.

Pour résumer on a :
- un arbitre de bus
- un seul type d'objet (en plus d'être périodique)
- un consommateur
- un producteur


Rentrons un peu plus dans la technique.

Il semblerait d'après ce que je comprends, que pour les objets périodiques, la configuration (c.'à-d. l'identifiant de l'objet, sa période, etc.) est connue au lancement du programme (il n'y pas une sorte de fetch sur le réseau). Donc à priori on stocke ces données dans un fichier par exemple (ou peu importe), que nos arbitre, consommateur, producteur chargent/connaissent à leur lancement. **(?)**

Ensuite suit l'échange de message, je copie bêtement le cours et j'en discute après :

>Le déroulement d’un échange de données s’effectue selon les étapes suivantes :
> 1. En utilisant sa table, l’arbitre de bus diffuse une trame (appelée ID-Dat) contenant l’identificateur d’un objet (il s’agit de l’objet que la table d’arbitre de bus indique comme étant l’objet à échanger à l’instant courant).
> 1. En “lisant” l’identificateur diffusé, le producteur et le(s) consommateur(s) de l’objet diffusé se reconnaissent.
> 1. Après un temps dit temps de retournement (fixé à quelques dizaines de μs pour un débit de 1 Mb/s), le producteur diffuse une trame (dite RP-Dat) contenant la valeur du tampon de production associé à l’objet dont l’identificateur a été diffusé par la dernière trame ID-Dat.
> 1. Le(s) consommateur(s) de l’objet met(tent) à jour la valeur de son (leur) tampon de réception à partir de la valeur contenue dans la trame RP-Dat.
> 1. Après un intervalle de temps égal au temps de retournement, l’arbitre de bus passe à l’identificateur suivant dans la sa table (quand le dernier identificateur de la table a été diffusé, l’arbitre de bus repart à partir du premier identificateur de la table).

Bon l'étape 5 nous sert à rien puisqu'on a qu'un seul type d'objet (faut qu'on se mette d'accord).
Sinon pour l'étape 3, le temps de retournement on le fixe à un temps quelconque ?  
D'après ce que je comprends, il n'y a pas d'acquittement (ACK). On peut toujours le rajouter pour le plaisir.

Pour l'implémentation, puisque que la transmission d'objets est basé sur du broadcast, il faut faire notre émulation soit sur de l'UDP (TCP supporte pas le broadcast logiquement). Vu qu'on a qu'un seul type d'objet, conso/producteur on peut aussi le faire en TCP (on aura une liste des IP) mais je pense qu'on perd une des idées du protocole qui est que les prod/conso ne connaissent pas qui est là et balance sur le réseau leurs objets.

Pour la forme des différentes trames (qu'on voit dans le cours de Zoubir. D'ailleurs, c'est pas exactement les mêmes que dans l'autre document, génial non ?), j'ai commencé à définir un objet dans `frame.py`, regarde les commentaires et dis-moi ce que tu en penses.

Dernier point (que je n'ai pas encore oublié) : je comprends pas l'histoire des LEDs.  
À aucun moment dans le cours il y a une idée de "temps de production", surtout que je vois pas à quoi ça correspond IRL, un capteur il met pas 200ans à recueillir sa donnée et l'envoyer non ? Il y a bien l'histoire du temps de transmission mais ça n'a pas l'air d'être ça dont il parle.  
Pareil pour le consommateur et son "temps de consommation". Bein il lit la valeur, la stocke et voilà ? Ça prend 1μs (et encore).

Ou alors il veut dire, que ce soit pour le conso ou le prod, que le temps de conso/prod correspond à la période de prod/conso (tous les coombiens c'est produit/consommé). Sauf que ça n'a pas vraiment de sens pour le conso vu que lui il sait juste qu'il doit consommer quand l'arbitre le lui dit (donc à priori pas de notion de période directement). De toutes façons les deux périodes doivent être synchro puisque l'arbitre a dans sa table une période unique pour un type d'objet donné.

Bref je comprends pas trop, help me plzz.