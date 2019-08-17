# Snake Machine Learning

![snake](https://user-images.githubusercontent.com/3957023/63204709-afcb9f80-c068-11e9-99f2-9b570e2e733c.png)

To Start, first run `python -m pip install -r './requirements.txt'` To get all of the requirements. (Note: This program right now only works in python version 3.6, not 3.7)

As of this version, there is no ui that ties everything together, it has to be done manualy (the ui is a WIP)

To play Snake:
  - Go to the snake.py file
  - Scroll all the way down to the bottom
  - Uncomment the very last line `# start()`
  - Run the snake.py file
  - Note: The point of this program is not to make a "good" version of snake, so playing the game manually isn't that great, for the best results hold down the keys when you are trying to turn
  
To run the genetic program:
  - Make sure that the start method in snake.py is commented out
  - Run the genetics.py file
  - You can change the parameters at the top of the file to change aspects of the run
    - `selection_rate`: the percentage of the population that will be used to breed the next generation (default = 0.1)
    - `mutation_rate`: the percentage that any gene (parameter) in a child will be mutated to a random value (default = 0.01)
    - `population_size`: the number of individuals that will be breed in each generation (default = 100)
    - `max_generations`: the number of generations that the program will run through (default = 100)
    - `show_graphics`: if true, you will see every individual run through and play the game until it dies, if false you won't see anything and it will just create the final model (default = True)
    - `save_population`: if true, the program will save the last generation so you can re run the program (default = False)
    - `save_best`: if true the program will save the best individual from each generation (default = False)
    - `save_graph`: if true the graph will be saved as a png (default = False)

Resources Used:
- <https://towardsdatascience.com/atari-solving-games-with-ai-part-2-neuroevolution-aac2ebb6c72b> Article on doing something similar with a different game
- <https://www.pygame.org/news> Graphics Library (only for game)
- <https://keras.io/> Neural Network library
- <https://github.com/gsurma/atari> Source for looking at an example of the genetic algorithms
- <https://kivy.org/#home> New Gui Library (Not for the game for now)
