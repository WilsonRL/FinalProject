# FinalProject

Capacitive Touch Augmentative and Alternative Communication (AAC) for dogs
Rebecca Wilson, McIntosh Webber

**Project summary**
In 2018, a speech-language pathologist taught her puppy to communicate by pressing buttons with prerecorded words including “outside,” “play” and “water.” Her dog currently uses over 45 different buttons in sequences of up to five words to communicate [1]. Many dog (and cat) owners have now taught their pets to communicate with recordable buttons and cognitive scientists are currently investigating the language capacity of non-human animals using recordable buttons along with video recordings of the animals using the buttons [2]. Our project aims to create a capacitive touch based augmentative and alternative communication (AAC) system for dogs and their owners that tracks the learner’s progress. 

**Goals and objectives**
There are several disadvantages to the currently available AAC systems for training dogs: (1) the buttons are large and take up a large amount of floor space, (2) the buttons can be difficult for smaller pets to press, (3) it can be difficult for the owner to hear the word being played if they're in a different room or it’s noisy and (4) there isn’t an automated way to track the button presses and learner’s progress. 
The goal of our final project is to address these issues by creating a capacitive touch based AAC system that can be used to train dogs to communicate and track their learning progress. More specifically, we plan to use Adafruit’s capacitive touch sensor breakout MPR121 - STEMMA QT) to create 12 capacitive touch based “buttons” that will each play a different word when touched, display the word(s) touched on the Raspberry Pi GUI and record and display a graphical representation of the number of times each word is pressed per day.  We will connect the sensor wirelessly to the Raspberry Pi and use a python library called gTTS to convert text-to-speech to generate the mp3 files.

**GPIO goals**
We will incorporate GPIO into our project by connecting a 12-channel capacitive touch sensor breakout (MPR121 - STEMMA QT) and a STEMMA Speaker to a Feather (RP2040) equipped with an AirLift FeatherWing ESP32 WiFi CoProcessor. We will add a button that downloads new mp3 files when pressed. We will refer to this wireless capacitive touch system as the “AAC board.”

**GUI goals**
The GUI will display a graphical representation of the number of the total times each words is pressed and the number of times each word is pressed per day. It also allows for user input of words to create the mp3 files and allow transfer to the AAC board.  
