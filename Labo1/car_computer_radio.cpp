#include <iostream>
#include <string>
#include <fstream>
#include <chrono>   // pour sleep_for
#include <unistd.h> // kbhit()
#include <termios.h>    // kbhit()
#include <fcntl.h>  // kbhit()
#include <thread>   // Labo 1
#include <mutex>    // Labo 1
#include <SFML/Audio.hpp>   // musique

using namespace std;
using namespace std::this_thread;
using namespace std::chrono;

// initialisation des fonctions
int kbhit(void);
void cligno(void);
void lyrics(void);
int music(void);

std::string line;   // variable globale pour afficher
std::ifstream file("lyrics.txt");   // variable pour verifier le fichier
std::mutex mtx; // variable du mutex

int main()
{   
    thread t1(lyrics);  // initalisation du thread lyrics
    thread t2(cligno);  // initalisation du thread clignotant
    thread t3(music);   // initalisation du thread musique

    cout << "----------Hi, starting playlist----------" << endl;
    while (true) {
        std::lock_guard<std::mutex> lock(mtx);  // bloque les thread pour ecrire dans la variable
        if (!line.empty()) {    // si la variable n'est pas vide
            std::cout << line << std::endl; // ecrit dans le terminal
            line.clear();   // efface ce qui est dans la variable
        }
    }
    t3.join();  // thread qui start la musique
    t2.join();  // thread qui start la detection des clignotant
    t1.join();  // thread qui start les lyrics
    cout << "----------Playlist completed, goodbye----------" << endl;
}

/*
*   Brief:
*   il detect si une touche est appuyer
*/
int kbhit() {
    struct termios oldt, newt;
    int ch;
    int oldf;

    // Save old terminal settings
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;

    // Set terminal to non-canonical mode
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    // Disable buffering on stdin
    setbuf(stdin, NULL);

    // Get file status flags
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    // Set file status flags to non-blocking
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    // Attempt to read from input
    ch = getchar();

    // Restore old terminal settings
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    // Restore old file status flags
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    // Check if a character was read
    if(ch != EOF) {
        // If a character was read, unget it back to stdin
        ungetc(ch, stdin);
        return 1;
    }

    return 0;
}

/*
*   Brief:
*   il s'active quand on appuye sur le 'l' ou 'r'
*/
void cligno(void) 
{
    char ch = ' ';
    while(true)
    {
        if(kbhit()) // si touche appuyer
        {   
            ch = getchar(); // prend la touche
            if(ch=='l'){    // si la touche est 'l'
                for (int i=0; i < 3; i++)   // le fait 3 fois
                {   
                    line = "Cligno gauche"; // ecrit dans la variable "cligno gauche"
                    sleep_for(milliseconds(1000));  // attend pendant 1sec
                } 
            }
            else if(ch=='r'){   // si la touche est 'r'
                for (int i=0; i < 3; i++)   // le fait 3 fois
                {   
                    line = "Cligno droit";  // ecrit dans la variable "cligno droit"
                    sleep_for(milliseconds(1000));  // attend pendant 1sec
                } 
            }
        }
    }
    
}

/*
*   brief:
*   il affiche les lyrics de la music 
*/
void lyrics(void)
{
    std::string lyrics;
    sleep_for(milliseconds(4500));  // start les paroles de la musique avec ceux afficher
    while (std::getline(file, lyrics)) {    // va lire la prochaine ligne
        line = lyrics;  //ecrit dans la ligne dans la variable
        sleep_for(milliseconds(1500));  // pause de la ligne avant la prochaine ligne
    }
}


/*
*   Brief: 
*   il va jouer la musique
*/
int music(void)
{
    sf::Music music;

    if(!music.openFromFile("soud of silence.ogg"))  // va lire le fichier
        return EXIT_FAILURE;    // sort s'il n'est pas capable de lire

    music.play();   // start la musique

    while(music.getStatus() == sf::Music::Playing); //reste dans la boucle avant de quitter

    return 0;
}