class Neuron:
    def __init__(self, value, bias):
        super().__init__()
        self.__value = value
        self.__bias = bias
        self.__total = 0

    def add_total(self, value):
        self.__total += value
    
    def set_total(self, value):
        self.__total = value

    def get_total(self):
        return self.__total

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def get_bias(self):
        return self.__bias
