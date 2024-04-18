![duck_logo](https://github.com/FelixDuck15/SOTR_H24/assets/89605334/5c092b82-f930-4e5f-bd92-b89e0f68a90b)

> Fait par: Félix-Antoine Guimont <br>
> Date: 18 avril 2024 <br>
> ISO: Linux <br>
> Logiciel: VSCode <br>
> Brief: Le code sert à faire bouger un robot dans une map prédéfini. Il y a 4 modes. Le premier est la statue, le deuxième est le control, <br>
> le troisième est le Kamikaze et le dernier est le Roomba. <br>


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
