# snake
Snake game this will be playable by humans and have a genetic machine learning part that will learn to play the game.

Links to start:
<https://towardsdatascience.com/atari-solving-games-with-ai-part-2-neuroevolution-aac2ebb6c72b> Article on doing something similar with a different game

<https://www.pygame.org/news> Graphics Library

<https://keras.io/> Neural Network library

<https://keras.io/#getting-started-30-seconds-to-keras> and <https://github.com/gsurma/atari/blob/master/convolutional_neural_network.py> Look at for learning how to create the CNN

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
- [ ] Machine learning
  - [ ] Create CNN (links above)
  - [ ] Get model to produce an output from a game state
    - [ ] Game State = array of the board that each have a number, 0 is blank, 1 is a wall, 2 is the snake (any part of it), 3 is the dot
    - [ ] Or Game State = {what is to left, what is to right, what is above} using same numbers
  - [ ] Create the genetic learning model to do the following:
    - [ ] Create the initial population (random models)
    - [ ] Breed two individuals together
    - [ ] Select the best individuals in the population (certain percent)
    - [ ] Mutate an individual (have random changes to specific parameters in the model)
    - [ ] Kill off the worse individuals and breed more until the population is back to its original size
  - [ ] Run and hope
- [ ] Display current progress
  - [ ] Display stats about the current generation (live updates? might run too fast)
  - [ ] Show a run through of the game given an individual
  - [ ] Show a list of options and view the game that it played
  - [ ] Graphs about increases in score over different generations
  
  
NOTES:
Input Shape = The grid thats already inplemented in the game, will be (right now) a square of size gridCount x gridCound
ex:
 [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 [1, 2, 2, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 0, 0, 0, 0, 3, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
 
 Action Space = ["Left", "Right", "None"] => Possible actions that the machine can do. Left and right will move left and right of the current direction that the snake is moving, none will cause the snake to do nothing and just move forward
