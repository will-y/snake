from confapp import conf
import settings

conf += settings

import pyforms
from pyforms_gui.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlText
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlLabel

from genetics import Genetics


class Main(BaseWidget):
    """
    parameters:
    selection_rate(0.1)
    mutation_rate(0.01)
    population_size(100)
    random_weight_range(1.0)
    max_generations(100)
    show_graphics(true)
    save_population(false)
    save_best(false)
    save_graph(true)
    """

    def __init__(self):
        super(Main, self).__init__('Snake Machine Learning')
        self.selection_rate = ControlText("Selection Rate (0.001-0.999)", default="0.1")
        self.mutation_rate = ControlText("Mutation Rate (0.001-0.999)", default="0.01")
        self.population_size = ControlText("Population Size (20-1000)", default="100")
        self.random_weight_range = ControlText("Random Weight Range (0.1 - 1.0)", default="1.0")
        self.max_generations = ControlText("Max Generations (1 - ...)", default="100")

        self.show_graphics = ControlCheckBox("Show Graphics", default=True)
        self.games_to_show = ControlText("Games to Show", default="25")
        self.grid_count = ControlText("Grid Count", default="30")
        self.grid_size = ControlText("Grid Size", default="5")

        self.save_population = ControlCheckBox("Save Population")
        self.save_best = ControlCheckBox("Save Best")
        self.save_graph = ControlCheckBox("Save Graph", default=True)

        self.error = ControlLabel("")
        self.start_button = ControlButton('Start Simulation')
        self.start_button.value = self.start_simulation

        self.formset = ['h1:Snake Machine Learning', 'h3:Machine Learning Parameters', 'selection_rate',
                        'mutation_rate',
                        'population_size', 'random_weight_range', 'max_generations',
                        'h3:Graphics Parameters', 'show_graphics', 'games_to_show', 'grid_count', 'grid_size',
                        'h3:Save Parameters', ('save_population', 'save_graph', 'save_best'),
                        'error', 'start_button']

    def start_simulation(self):
        print(self.save_population.value)
        if self.check_variables():
            Genetics(replay=False, runId=1, load_pop=False, selection_rate=float(self.selection_rate.value),
                     mutation_rate=float(self.mutation_rate.value),
                     population_size=int(self.population_size.value),
                     random_weight_range=float(self.random_weight_range.value),
                     max_generations=int(self.max_generations.value),
                     show_graphics=self.show_graphics.value,
                     games_to_show=int(self.games_to_show.value),
                     grid_count=int(self.grid_count.value),
                     grid_size=int(self.grid_size.value),
                     save_population=self.save_population.value,
                     save_graph=self.save_graph.value,
                     save_best=self.save_best.value)

    def check_variable(self, name, value, min_value, max_value, variable_type):
        # integer
        if variable_type == 0:
            if self.isInt(value):
                if int(value) < min_value or int(value) > max_value:
                    self.show_var_error(name, min_value, max_value, variable_type)
                    return False
            else:
                self.show_error(name + "needs to be an integer")
        # float
        elif variable_type == 1:
            if self.isFloat(value):
                if float(value) <= min_value or float(value) >= max_value:
                    self.show_var_error(name, min_value, max_value, variable_type)
                    return False
            else:
                self.show_error(name + "needs to be a float")
        else:
            return False

        self.show_error(" ")
        return True

    def check_variables(self):
        return (not self.check_variable("selection_rate", self.selection_rate.value, 0, 1, 1)
                and not self.check_variable("mutation_rate", self.mutation_rate.value, 0, 1, 1)
                and not self.check_variable("population_size", self.population_size.value, 20, 1000, 0)
                and not self.check_variable("random_weight_range", self.random_weight_range.value, 0.1, 1.0, 1)
                and not self.check_variable("max_generations", self.max_generations.value, 1, -1, 0)
                and not self.check_variable("games_to_show", self.games_to_show.value, 1, self.population_size.value, 0)
                and not self.check_variable("grid_count", self.grid_count.value, 3, 10000, 0)
                and not self.check_variable("grid_size", self.grid_size.value), 1, 1000, 0)

    def show_var_error(self, var, min_value, max_value, variable_type):
        self.show_error(var + " must be between " + str(min_value) + " and " + str(max_value))

    def show_error(self, message):
        self.error.value = message

    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isInt(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    pyforms.start_app(Main, geometry=(200, 200, 1, 1))
