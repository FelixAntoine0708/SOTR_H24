
#### Auteur : Carl-Dominc Aubin & Félix-Antoine Guiont
#### Date : Jeudi 23 avril 2024
#### Cours : Système ordinés temps réel
#### Révision : 1.0 du Cégep de Sherbrooke

<br />

# Projet 2 - robot first

<br />


## Mise en contexte
### Description
Ce script simule une partie de robot first. Le but est de faire le plus de points dans le temps respecté. Pour faire des points, il faut récuprer un ballon et le lancer dans le panier au centre du terrain. Il est aussi possible de faire des points en escaladant les barreaux situer dans le coin respectif de chaque robot. Les robots possède les mêmes fonctions que les derniers laboratoires, soit un laser qui empêche les collisions. Le code est séparé en 2 partie, soit le contrôle des robots et l'autre du terrain. Les deux programmes communiquent à l'aide de topic et suscribe et publish pour obtenir de l'information du terrain et vice-versa.

### Version

La version de python utilisé est python 3.8

La version de ros utilisé est noetic

L'image de luduntu est 20.04

## Dépendances/Installation

tqdm - pour les barres de progressions

pygame - pour la fluidité des mouvements

### Software

Si vous n'avez pas installé ross noetic : https://wiki.ros.org/noetic/Installation/Ubuntu 

Vous devez aussi installer python si ce n'est pas déjà fait, voir le tutoriel ci-haut

Suivre les étapes jusqu'à la création ROS workspace

$ catkin_create_pkg robot_first std_msgs nav_msgs rospy sensor_msgs std_msgs tf

Recette pour l'ajout d'un nouveau noeud ROS dans un "package":

Ouvrir le fichier CMakeList.txt pour votre "package courant" et aller à la fin : /home/tge/catkin_ws/src/"nom du package"/CMakeList.txt

Ajouter une entrée pour chaque nouveau fichier .py que vous voulez utiliser dans ROS: ex: catkin_install_python(PROGRAMS scripts/nouveau_noeud.py  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}

exemple :
catkin_install_python(PROGRAMS
src/Robot_First.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

Lancer un terminal et exécuter la commande catkin_make à partir du répertoire (/home/tge/catkin_ws) 

### Hardware

Ordinateur/laptop recommandation : 
- 16g de RAM
- processeur minimum 2 coeurs

### Get started

Après avoir ajouté le fichier.py à votre cmake file, vous pouvez ouvrir la carte visuel, il faut d'abord ouvrir un core pour ros avec :
```sh
roscore ou roscore& 
```
& vous laisse utiliser ce terminal, pendant que roscore s'effectue dans le background

Ensuite, lancer la carte que vous avez téléchargé, aller premièrement dans le répertoire en question
```sh
rosrun stage_ros stageros robot_first/stageworld/first_double.world
```
Vous devriez voir une carte avec un point qui correspond à votre romba. Vous pouvez appuyer sur 'd' pour faire apparaître votre laser.

Tout en restant de le répertoire cible, exécuter votre code en python pour 


*Vous pouvez aussi utiliser vscode pour déboguer et apporter des modifications à votre code, cela jusqu'à un certain d'utilisation de thread, il est ensuite recommandé d'utiliser des prints et de démarrer le programme à l'aide de rosrun pour assurer la fonctionnalité entre thread*

## Utilisation

### cmd 
#### Contrôle pour robot 1
- W : Avancer
- S : Reculer
- A : Tourner à gauche
- D : Tourner à droite
- Z : Charger un ballon
- X : Lancer un ballon  
- C : Grimper

#### Contrôle pour robot 2
- I : Avancer
- K : Reculer
- J : Tourner à gauche
- L : Tourner à droite
- B : Charger un ballon
- N : Lancer un ballon  
- M : Grimper

#### Réglage de la partie
- 1 : Départ du match
- 2 : Mode autonome
- 3 : Mode téléopérée
- 4 : Arrêt du match
- 0 : Arrêt complet

## Commande ros utile

*vous devez être dans le répertoire catkin_ws/src/*

Pour voir les nodes actifs sur votre roscore
```sh
rosnode list
```
Pour voir les topics actifs sur vos nodes
```sh
rostopic list
rostopic echo <<topic name>>
```
Pour voir l'architecture de vos nodes et topics
```sh
rqt_graph
```

## License

Ce programme est complètement open-source