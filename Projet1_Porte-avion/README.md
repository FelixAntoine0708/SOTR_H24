
#### Auteur : Félix-Antoine Guimont & Carl-Dominc Aubin
#### Date : Jeudi 7 mai 2024
#### Cours : Système ordinés temps réel
#### Révision : 1.0 du Cégep de Sherbrooke

<br />

# Projet 1 - Porte-avions

<br />


## Mise en contexte
### Description
Ce script Python simule les ressources à gérer sur un porte avions. Les ressources à contrôler sont les 4 catapultes de lancement. Il est possible de lancer les avions à l'aide des 4 catapultes 


### Version

La version de python utilisé est python 3.8

L'image de luduntu est 20.04 sur VMware

## Dépendances/Installation

### Software

Vous devez aussi installer python si ce n'est pas déjà fait, voir le tutoriel ci-haut

$ sudo apt-get update
$ sudo apt-get install python3

### Hardware

Ordinateur/laptop recommandation : 
- 16g de RAM
- processeur minimum 4 coeurs 

### Get started

Pour débogger le programme avec vscode, lancer le programme en mode débogage, ensuite entrer en tant que root (su) et appuyer sur Fn+F5 pour entrer en mode déboggage en tant que root, cela va empêcher les erreurs d'accès au library root (accèes au clavier)

*Vous pouvez aussi utiliser vscode pour déboguer et apporter des modifications à votre code, cela jusqu'à un certain d'utilisation de thread, il est ensuite recommandé d'utiliser des prints et de démarrer le programme à l'aide de rosrun pour assurer la fonctionnalité entre thread*

## Utilisation

### cmd 

#### Contrôle
- 1 : Fermer catapule avant
- 2 : Ouvrir catapulte avant
- 3 : Fermer catapulte côté
- 4 : Ouvrir catapulte côté
- l : Lancer un avion
- r : Retour de tous les avions
- s : État des avions
- v : Catapulte disponible
- q : Quitter le programme (dois ramener tous les avions avant)

#### Logique 

***Se référer à Navire.png pour comprendre la logique du porte avions***

Si une catapulte est en maintenance, les deux catapultes d'une section seront bloquées. Lorsque les catapultes de côtés sont en maintenance, il est imposible d'attérir des avions et seulement 1 avions peut attérir à la fois et cela en tout temps. Une limite de 30 avions se retrouve sur le porte avion. Un avion prend 10 sec à décoler et 20 sec à attérir. Il est possible de catapulter 4 avions à la fois.

## Commandes utiles

htop (vous pouvez voir la consommation en mémoire de votre programme)

## License

Ce programme est complètement open-source