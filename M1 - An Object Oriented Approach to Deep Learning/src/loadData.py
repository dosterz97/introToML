# ?: boolean
# h: short
# l: long
# i: int
# f: float
# q: long long int

import struct
from NeuralNet import NeuralNet

# 0000     32 bit integer  0x00000803(2051) magic number
# 0004     32 bit integer  60000            number of images
# 0008     32 bit integer  28               number of rows
# 0012     32 bit integer  28               number of columns

IMG_WIDTH = 28
IMG_HEIGHT = 28
IMG_SIZE = IMG_WIDTH * IMG_HEIGHT
PRINT_BYTE_ARRAY_AS_NUMBERS = True
DRAW_THRESHOLD = 100 # if byte value (0-255) is above 100 consider it "on"

def load_training_binary_file():
    net = NeuralNet()
    net.initialize_with_random_weights()

    labels_file = open('../data/train-labels-idx1-ubyte', mode='rb')
    with open('../data/train-images-idx3-ubyte', mode='rb') as file:
        fileContent = file.read()
        labels_file_content = labels_file.read()
        data_info = struct.unpack('iiii', fileContent[:16])
        label_info = struct.unpack('ii', labels_file_content[:8])

        magic_number = data_info[0]
        number_of_images = data_info[1]
        number_of_rows = data_info[2]
        number_of_columns = data_info[3]

        labels_magic_number = data_info[0]
        labels_number_of_items = data_info[1]

        # meta info
        print(data_info)
        print(label_info)

        index = 16
        label_index = 8
        
        for number in range(0, number_of_images):
            byte_array = struct.unpack('B' * IMG_SIZE, fileContent[index: index + IMG_SIZE])
            
            try:
                label = struct.unpack('B', labels_file_content[label_index: label_index + 1])[0]
            except:
                x = 0
            if PRINT_BYTE_ARRAY_AS_NUMBERS:
                print("label: ", label)
                print_byte_array_like_a_number(byte_array)
                net.input_image(byte_array, label)

            label_index += 1
            index += IMG_SIZE
            print("\n---------------------------------")


def print_byte_array_like_a_number(row_data):
    for index, byte in enumerate(row_data):
        # newline
        if index % IMG_WIDTH == 0:
            print("")
        if byte > DRAW_THRESHOLD:
            print("1", end="")
        else:
            print("0", end="")
        



load_training_binary_file()