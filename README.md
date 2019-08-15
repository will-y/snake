# snake
Snake game this will be playable by humans and have a genetic machine learning part that will learn to play the game.

Links to start:
<https://towardsdatascience.com/atari-solving-games-with-ai-part-2-neuroevolution-aac2ebb6c72b> Article on doing something similar with a different game

<https://www.pygame.org/news> Graphics Library (only for game)

<https://keras.io/> Neural Network library

<https://keras.io/#getting-started-30-seconds-to-keras> and <https://github.com/gsurma/atari/blob/master/convolutional_neural_network.py> Look at for learning how to create the CNN
<https://kivy.org/#home> New Gui Library (Not for the game for now)

TODO:
- [x] Create Game
  - [x] Draw Board
  - [x] Draw Snake
  - [x] Move Snake Around
  - [x] Die if hit side
  - [x] Spawn things to eat
  - [x] Eating grows snake
  - [x] Hiting self kills you
  - [x] Score counter
  - [x] Have game run in ticks and be able to set tick speed so that machine learning can be faster
- [x] Machine learning
  - [x] Create NN (links above)
  - [x] Get model to produce an output from a game state
    - [x] Game State = array of the board that each have a number, 0 is blank, 1 is a wall, 2 is the snake (any part of it), 3 is the dot
    - [ ] ~~Or Game State = {what is to left, what is to right, what is above} using same numbers~~
  - [x] Create the genetic learning model to do the following:
    - [x] Create the initial population (random models)
    - [x] Breed two individuals together
    - [x] Select the best individuals in the population (certain percent)
    - [x] Mutate an individual (have random changes to specific parameters in the model)
    - [x] Kill off the worse individuals and breed more until the population is back to its original size
  - [x] Run and hope
- [ ] Display current progress
  - [x] Display stats about the current generation (live updates)
  - [x] Show a run through of the game given an individual
  - [ ] Show a list of options and view the game that it played
  - [x] Graphs about increases in score over different generations
  
  
NOTES:
Input Shape = a list with length 16. Will include the distance to food and distance to itself/wall in every direction:
   N     NE     E      SE      S      SW     W     NW
[4, 4, 3, -1, 5, -1, 7, -1, 6, -1, 10, -1, 5, -1, 6, -1]
 
 Action Space = ["up", "down", "left", "right"]: The four directions that the snake can move in, going forward or backwards from the current direction won't do anything
