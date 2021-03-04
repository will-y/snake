import pygame as pg
import sys
import math

class NetworkDisplay():
    layer_width = 70
    layer_height = 700
    layer_box_x_padding = 15 
    layer_box_y_padding = 50
    node_size = 20
    node_padding = 20
    x_padding = 50
    node_color = pg.Color(0, 0, 255)
    layer_color = pg.Color(255, 255, 255)
    background_color = pg.Color(0, 0, 0)
    connection_color = pg.Color(255, 0, 0)

    def __init__(self, network):
        self.network = network.layers
        pg.init()
        self.screen = pg.display.set_mode((1000, 700))
        self.screen.fill(self.background_color)
        self.display_loop()

    def display_loop(self):
        while True:
            # If x clicked, don't crash
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    sys.exit()

            for i in range(1, len(self.network)):
                self.draw_connections(self.network[i], self.network[i - 1], i)
            
            for i in range(len(self.network)):
                self.draw_nodes(self.network[i], i)

            pg.display.flip()

        
    def draw_nodes(self, layer, number):
        nodes_in_layer = len(layer)
        vertical_padding = math.floor((self.layer_height - (self.node_size * 2 + self.node_padding) * nodes_in_layer + self.layer_box_y_padding) / 2)
        # draw layer box
        pg.draw.rect(self.screen, self.layer_color, (self.x_padding + number * (self.layer_width + self.layer_box_x_padding) - self.layer_width / 2, self.layer_box_y_padding, self.layer_width, self.layer_height - (self.layer_box_y_padding * 2)), 1)

        # draw nodes and the connections
        for i in range(nodes_in_layer):
            node_pos = (self.x_padding + number * (self.layer_width + self.layer_box_x_padding), (self.node_padding + self.node_size * 2) * i + vertical_padding)
            pg.draw.circle(self.screen, self.node_color, node_pos, self.node_size)

    def draw_connections(self, layer, prev_layer, number):
        nodes_in_layer = len(layer)
        vertical_padding = math.floor((self.layer_height - (self.node_size * 2 + self.node_padding) * nodes_in_layer + self.layer_box_y_padding) / 2)
        prev_vertical_padding = math.floor((self.layer_height - (self.node_size * 2 + self.node_padding) * len(prev_layer) + self.layer_box_y_padding) / 2)

        # draw nodes and the connections
        for i in range(nodes_in_layer):
            node_pos = (self.x_padding + number * (self.layer_width + self.layer_box_x_padding), (self.node_padding + self.node_size * 2) * i + vertical_padding)

            # draw the connections to the next layer
            for j in range(len(prev_layer)):
                pg.draw.line(self.screen, self.connection_color, node_pos, (self.x_padding + (number - 1) * (self.layer_width + self.layer_box_x_padding), (self.node_padding + self.node_size * 2) * j + prev_vertical_padding), 1)
        