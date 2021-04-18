import Neuron

class Connection:
    def __init__(self, neuron_1, neuron_2, weight):
        super().__init__()
        self.__neuron_1 = neuron_1
        self.__neuron_2 = neuron_2
        self.__weight = weight

    def get_neuron_1(self):
        return self.__neuron_1
    
    def get_neuron_2(self):
        return self.__neuron_2

    def get_weight(self):
        return self.__weight