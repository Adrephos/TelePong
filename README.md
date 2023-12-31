# Project 1 - Telematics course

## 1. Introduction 

<!-- <img src="https://github.com/Adrephos/TelePong/assets/83888452/deaebd1f-125e-48bd-8b5c-1bcc8c3874a9" width="320" height="180" alt="Image"> -->

Telepong is an online game that recreates the game Pong, famous for being the first videogame in history. The game allows users to register with a username and email, and to create a room to play with friends.  
The game has its own communication protocol and a more modern interface made with Python. 

![pongProtocol](https://github.com/Adrephos/TelePong/assets/83888452/5f60af2b-ee0c-459e-9fac-269ce2a42998)

<img src="https://github.com/Adrephos/TelePong/assets/83888452/9b06da49-3b23-433f-bcf3-ad075d7d1cf7" width="640" height="360" alt="Image">

<img src="https://github.com/Adrephos/TelePong/assets/83888452/cfb1e5c3-47b7-44d2-823a-e967fd2ffb22" width="640" height="360" alt="Image">


## 2. Running the project
1. Make sure you have `C`,`Python` and `Makefile` related tools and libraries installed in your system
2. At a terminal, create a folder and run a `git clone` inside of it with the project's Github URL. Then, Navigate to the project directory with `cd TelePong`
3. Navigate to the server folder with `cd Server` and create a folder `obj`. Then, run the Make cript with `Make`
4. Execute the compiled code. Navigate to bin folder with `cd bin` and run the command `./PongServer 8080 ../logs/logfile.txt`. 8080 is the desired port to be used and ../logs/logfile.txt the path for the logfile
   
   ![image](https://github.com/Adrephos/TelePong/assets/83888452/32252945-727c-48f5-8270-53c888c9d385)

6. Navigate to the client folder. `cd ../..` and then `cd client`
7. Recommended: run the Python code in a virtual enviroment. To create the virtual enviroment, use the command `python -m venv venv` and active it with `source venv/bin/activate`
8. Install the needed dependencies with `pip install pygame` and `pip install pygame_gui`
9. Execute the python code with `python game.py`
   
   ![image](https://github.com/Adrephos/TelePong/assets/83888452/2d5978cc-042d-460b-a2bf-46851b194041)

## 3. Development - Definition of the protocol - TCP or UDP
We had to decide whether to use the TCP or UDP protocol as the foundation for our project. At the end, we opted to use TCP, due that with the UDP protocol, despite the advantage of being faster, is not convinient since it could trigger lost packages and desynchronization between the players. With TCP we garantee that every package is delivered correctly and in the right order

### Structure of the project:
### Client:
- assets folder: recourses needed for the game, such as images and font
- constants: values that remain static throughout the program, such as the used IP and Port
- tpp (TelePong Protocol): class with the functions that define the comunication between client and server
- game: everything related with the game

### Server:
- bin folder: contains the executable of the server
- include folder: defines the header files, which contains the declaration of functions that may be used in other parts of the code
- logs folder: in this folder the logs.txt file is generated 
- obj folder: contains the .o files, generated during the compilation of the code
- src folder: contains the main C code

## 4. Conclusions 
- The choice of using TCP led to some delay issues
- The project could have better code practices and optimization, like the use of an interface between game.py and tpp.py to decouple the code and stop the direct dependency. In addition, that way every game would use the same instance of the tpp class, unlike how we have it at the moment where every game has a tpp instance.
- Design choices and careful consideration of the problem before coding are crucial. We were able to develop the project the way we did because we first readed about both protocols and their advantages and disadvatages, we thought how to develop the solution, how to structure a project in C and created the diagrams. Without these preparations, the project development would have been significantly more challenging. 

## 5. References
This project could not have been possible without some resources that we found in the internet

- General structure of the game: https://www.geeksforgeeks.org/create-a-pong-game-in-python-pygame/
- Screen menu system: https://github.com/baraltech/Menu-System-PyGame
- Text input: https://github.com/baraltech/Text-Input-PyGame

