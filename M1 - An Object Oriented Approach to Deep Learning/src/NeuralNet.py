import math
import random
import numpy as np

from Neuron import Neuron
from Connection import Connection

INPUT_NEURON_SIZE = 784
SECOND_ROW_SIZE = 16
THIRD_ROW_SIZE = 16
OUTPUT_ROW_SIZE = 10

class NeuralNet:
    def __init__(self):
        super().__init__()

        self.__correct = 0
        self.__incorrect = 0
        self.__total = 0
        self.__input_neurons = [None] * INPUT_NEURON_SIZE
        self.__input_to_second_row_connections = [None] * INPUT_NEURON_SIZE * SECOND_ROW_SIZE
        self.__second_row = [None] * SECOND_ROW_SIZE
        self.__second_to_third_row_connections = [None] * SECOND_ROW_SIZE * THIRD_ROW_SIZE
        self.__third_row = [None] * THIRD_ROW_SIZE
        self.__third_to_output_row_connections = [None] * THIRD_ROW_SIZE * OUTPUT_ROW_SIZE
        self.__output_row = [None] * OUTPUT_ROW_SIZE

    # 0 - 255 to 0.0 -> 1.0
    def normalize_byte_number(self, value):
        return value / 255.0

    def initialize_with_random_weights(self):
        for index in range(0, INPUT_NEURON_SIZE):
            # 0 bias for first set
            self.__input_neurons[index] = Neuron(0, 0)

        for index in range(0, SECOND_ROW_SIZE):
            self.__second_row[index] = Neuron(0, 0)
            for input_index in range(0, INPUT_NEURON_SIZE):
                # create connection 
                # Note: random is [0.0 to 1.0)
                weight = self.get_random_weight()
                neuron_1 = self.__input_neurons[input_index]
                neuron_2 = self.__second_row[index]
                connection_index = index * INPUT_NEURON_SIZE + input_index
                self.__input_to_second_row_connections[connection_index] = Connection(neuron_1, neuron_2, weight)

        for index in range(0, THIRD_ROW_SIZE):
            self.__third_row[index] = Neuron(0, 0)
            for second_row_index in range(0, SECOND_ROW_SIZE):
                # create connection 
                # Note: random is [0.0 to 1.0)
                weight = self.get_random_weight()
                neuron_1 = self.__second_row[second_row_index]
                neuron_2 = self.__third_row[index]
                connection_index = index * SECOND_ROW_SIZE + second_row_index
                self.__second_to_third_row_connections[connection_index] = Connection(neuron_1, neuron_2, weight)

        
        for index in range(0, OUTPUT_ROW_SIZE):
            self.__output_row[index] = Neuron(0, 0)
            for third_row_index in range(0, THIRD_ROW_SIZE):
                # create connection 
                # Note: random is [0.0 to 1.0)
                weight = self.get_random_weight()
                neuron_1 = self.__third_row[third_row_index]
                neuron_2 = self.__output_row[index]
                connection_index = index * THIRD_ROW_SIZE + third_row_index
                self.__third_to_output_row_connections[connection_index] = Connection(neuron_1, neuron_2, weight)
            

    def input_image(self, byte_array, label):
        # assign to first layer
        for index, neuron in enumerate(self.__input_neurons):
            neuron.set_value(byte_array[index])
        
        # run through input to second row connections
        self.compute_next_row(self.__input_to_second_row_connections)

        # run through second to third row connections
        self.compute_next_row(self.__second_to_third_row_connections)

        # run through third to output row connections
        self.compute_next_row(self.__third_to_output_row_connections)

        # calculate cost
        self.calculate_cost(label)
        # # get largest value from output connection
        # # print(self.__output_row)
        # print("\nlabel: ", label)
        # best = 0
        # for index, neuron in enumerate(self.__output_row):
        #     best = index if neuron.get_value() > self.__output_row[best].get_value() else best
        #     print(str(index) + ": " + str(neuron.get_value()))

        # print('best: ', best)

        # # update statistics
        # self.update_statistics(best, label)

    def update_statistics(self, best, label):
        if best == label:
            self.__correct += 1
        else:
            self.__incorrect += 1
        
        self.__total += 1

    def compute_next_row(self, connections):
        # sum up all connections leading to next row
        for connection in connections:
            n1 = connection.get_neuron_1()
            n2 = connection.get_neuron_2()

            # print("n1 value: ", str(n1.get_value()))
            # print("weigth: ", str(connection.get_weight()))
            computed_value = n1.get_value() * connection.get_weight()
            n2.add_total(computed_value)

        # now that the values are sigma(weight(i)*value(i))
        # apply bias and sigmoid function to each one
        for connection in connections:
            # reset the last row i think?
            n1 = connection.get_neuron_1()
            n1.set_total(0)
            n1.set_value(0)

            # compute sigmoid value
            n2 = connection.get_neuron_2()
            raw_value = n2.get_total()
            bias_value = raw_value - n2.get_bias()
            # if bias_value > 1 or bias_value < -1:
            #     print(bias_value)
            normalized_value = self.sigmoid(bias_value)
            n2.set_value(normalized_value)

        return True
            

    def sigmoid(self, x):  
        return math.exp(-np.logaddexp(0, -x))

    def get_random_weight(self):
        return random.uniform(-1, 1)

    def calculate_cost(self, expected_output):
        cost = 0
        expected = [0] * OUTPUT_ROW_SIZE
        expected[expected_output - 1] = 1
        
        for index, neuron in enumerate(self.__output_row):
            value = neuron.get_value()

            cost += (value - expected[index])**2



    
    def back_propogate(self):

        print("bleh")