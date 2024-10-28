**Implementation A\* pour l'Ane Rouge**


Dependences not built-in:
- Colorama


Pour lancer le script, executer main.py, l'execution se fait dans le terminal,
laisser de la place pour l'affichage de la solution qui prend une bonne centaine de lignes.

Pour l'instant la recherche est très lente, pour cause le fait que je n'arrive pas a trouver une
heuristique satisfaisante. La solution n'est donc pas non plus optimale, mais pas mauvaise non plus (~110 op, le meilleur est ~90)

*Probleme de l'heuristique :*
Le jeu de l'Ane rouge se base sur le fait d'effectuer de nombreuses operations qui semblent eloignées du but, pour ensuite arriver a faire baisser le cube rouge.
Le probleme est que si on se ramene a lheuristique suivante: plus le cube rouge est bas, plus c'est bien, on se retrouve juste a assayer toutes les combinaisons pour faire baisser le cube rouge, car on n'a aucune autre heuristique.
Les autres heuristiques, qui proposent de liberer la place autour du cube rouge, ou alors essayer de mettre un minimum de pieces qui genent, sont assez futiles car il n'y a que 2 espaces libres sur le plateau, 
et le but est de s'arranger de maniere detournée pour avancer jusqu'au but.
Je me demande donc si l'algorithme A* est vraiment la bonne solution pour resoudre ce jeu, en un temps rapide, du au flou dans lequel on est pour la majorité du jeu, et des actions possibles.
Certe la solution est satisfaisante, mais pas le temps pour la trouver: un brut force, avec un peu de chance, serait meilleur.
Ah moins de trouver une heuristique miracle, le combinaison lineaire simple d'heuristiques citées precedemment ne semble pas avoir un impact majeur sur la perfomance, si ce n'est que du resusltat, qui passe ici en deuxieme.
