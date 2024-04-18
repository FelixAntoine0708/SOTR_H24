![alt text](C:\Users\Utilisateur\Pictures\logo_duck.jpg)

# Comment fonctionne le labo 3 et 4

## Créer un package

* Aller dans le dossier `catkin_ws/src`
```
cd ~/catkin_ws/src
```

* Créer le package 
```
catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
```

* Prener le dossier `Script` 

* Aller le mettre dans le package que vous venez de créer
```
cd ~/catkin_ws/src/<package_name>/src
```
> [!NOTE]  
> Vérifier si le fichier dans le dossier `Script` est executable 
> Sinon suiver les étapes suivante:
> ```
> cd ~/catkin_ws/src/<package_name>/src/Script
> chmod +x <file_name> 
> ```

* Créer le dossier de travail et sourcer les fichier d'installation
``` 
cd ~/catkin_ws/
catkin_make
source /devel/setup.bash 
```

## Faire fonctionner le code
* Prener le dossier et metter le dans dossier Documents
```
cd ~/Documents
```

* Ouvrer un terminal sur linux

* spliter en 3 le terminal

* Dans le premier écriver
```
roscore
```

* Dans le deuxième écriver
```
rosrun stage_ros stageros ~/Documents/
```

* Dans le troisième écriver 
```
cd ~/catkin_ws/src/

rosrun <package_name> custom_teleopkeyLabo3.py

ou 

rosrun <package_name> custom_teleopkeyLabo4.py
```
