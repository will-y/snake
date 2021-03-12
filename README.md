# Snake Machine Learning

![snake](https://user-images.githubusercontent.com/3957023/63204709-afcb9f80-c068-11e9-99f2-9b570e2e733c.png)

To Start, first run `python -m pip install -r './requirements.txt'` To get all the requirements. (Note: This program right now only works in python version 3.6, not 3.7)


To play Snake:
  - Go to the legacy branch to play the game yourself
  
To run the genetic program:
  - Make sure that the start method in snake.py is commented out
  - Run the main.py file
  - You can change the parameters in the UI that launches
    - `selection_rate`: the percentage of the population that will be used to breed the next generation (default = 0.1)
    - `mutation_rate`: the percentage that any gene (parameter) in a child will be mutated to a random value (default = 0.01)
    - `population_size`: the number of individuals that will be bred in each generation (default = 100)
    - `random_weight_range`: the range of the weights that are generated for the initial population (default = 1.0)
    - `max_generations`: the number of generations that the program will run through (default = 100)
    - `show_graphics`: if true, you will see every individual run through and play the game until it dies, if false you won't see anything and it will just create the final model (default = True)
    - `games_to_show`: the number of games to show at a time (default = 25)
    - `grid_count`: the number of grids in the actual snake games (default = 30)
    - `grid_size`: the size of each square in the snake game grids (default = 5)
    - `save_population`: if true, the program will save the last generation, so you can re-run the program (default = False)
    - `save_best`: if true the program will save the best individual from each generation (default = False)
    - `save_graph`: if true the graph will be saved as a png (default = True)

Resources Used:
- <https://towardsdatascience.com/atari-solving-games-with-ai-part-2-neuroevolution-aac2ebb6c72b> Article on doing something similar with a different game
- <https://www.pygame.org/news> Graphics Library (only for game)
- <https://keras.io/> Neural Network library
- <https://github.com/gsurma/atari> Source for looking at an example of the genetic algorithms
- <https://kivy.org/#home> New Gui Library (Not for the game for now)
