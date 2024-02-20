# Comment utiliser le code du Labo 1 - SOTR
***
* Aller sur une vm Linux et utiliser VScode
* Prend prend le fichier 
`car_computer_radio.cpp`, 
`lyrics.txt` et
`soud of silence.ogg`
* Installer la librarie SFML
  ```
  sudo apt-get install libsfml-dev
  ```
* Ajouter le dossier Audio_SFML dans
  `/home/"your_user"`
* Ajouter les lignes dans le fichier
   `task.json`
  ```
  "-pthread",
  "-lsfml-audio"
  ```
* Dans le terminal de VScode fait les 3 lignes de commande suivantes:
  ```
  g++ -c car_computer_radio.cpp -I /home/"your_user"/Audio_SFML
  g++ car_computer_radio.o -o sfml-app -lsfml-audio -pthread
  ```
* un fichier `sfml-app` et `car_computer_radio.o` va être créé.
* Dans le terminal de VScode fait la ligne suivante:
  ```
  ./sfml-app
  ```
* Voilà le code fonctionne
