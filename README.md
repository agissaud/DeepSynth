# Logo DSL

L'objectif de ce dépot est d'implémenter un nouveau Domain Specific Language (DSL) centré sur les logos au framework Deep Synth.

## Liste des fichiers et descriptions :

1. DSL/logo.py : Ce fichier contient la définition du DSL logo. C'est à dire la définition des primitives et du lien vers leur sémantique. La grande partie des fonctions de sémantique sont définies dans le fichier "shape.py" 

2. shape.py: Ce fichier contient les définitions pour les types "Shape" utilisés dans le DSL. L'approche utilisée est la programmation orientée objet. Ainsi, on retrouve la classe mère "Shape" et tous les formes basiques utilisées par le DSL (rectangle, cercle et polygone) sont des classes filles de Shape.

3. Fichiers auxiliaires:
    - experiment_helper_logo: contient les fonctions d'aides au traitement des logos. On y retrouve des fonctions utilisées pour évaluer la qualité des logos générés.
    - run_experiment_logo: contient des tests du DSL mais également une boucle de génération de logos. Ce fichier peut être executé pour avoir un aperçu du DSL.

## Notes

Le DSL fonctionne principalement en utilisant une liste interne d'objets "shape". Ainsi, il faut manipuler cette liste pour utiliser le DSL. La liste des méthodes concernant cette liste se trouve dans "shape.py":
- draw_all_shape_show(): Affiche le logo correspondant à la liste interne.
- draw_all_shape(): Retourne un objet Image correspondant à la liste interne ou bien la liste passée en paramètre.
- clear_list_shape(): Vide la liste interne. Fonction à utiliser entre deux évaluation de logos si l'on souhaite qu'il ne s'additionne pas.
- print_list_shape(): Affiche la liste interne.


## Potentielles améliorations

La prochaine étape d'intégration du DSL est la création d'un dataset de logos pour pouvoir entrainer le modèle générant la PCFG. Pour cela, il faut pouvoir sélectionner des logos pertinents parmi les logos générés. La boucle de génération dans "run_experiment_logo" écarte déjà les logos qui ont moins de 3 formes utilisées et ceux dont au moins l'une des formes utilisées dans le logo est dispensable. \
Une autre piste est d'empêcher des formes. Par exemple, on souhaite ne pas avoir de rectangles avec une largeur nulle ou bien des polygones à 0 cotés.


## Problèmes connus

Le déplacement des "shape" via la méthode "move" est un déplacement relatif par rapport à l'objet shape. Cependant, le DSL Logo n'utilise que les chiffres de 0 à 9 et la position initial des objets shape est au centre. Les programmes générés ne peuvent donc pas déplacer les formes vers le haut ou la gauche car il faudrait des nombres négatifs. \
Deux solutions envisageables :
- Ajouter des nombres négatifs au DSL. Il faudra alors empêcher de créer des formes avec des paramètres négatifs (comme un polygone avec -5 cotés).
- Changer la fonction move pour un déplacement par position absolue.

Il n'est pas possible d'effectuer la rotation d'un rectangle car cela n'est pas permis par la bibliothèque utilisé.

# DeepSynth

Lien vers le projet Deep Synth:
[https://github.com/nathanael-fijalkow/DeepSynth/](https://github.com/nathanael-fijalkow/DeepSynth/)