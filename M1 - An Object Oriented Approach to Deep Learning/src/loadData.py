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

        print(data_info)
        print(label_info)


        index = 16
        label_index = 8
        bleh = False
        for number in range(0, number_of_images):
            byte_array = struct.unpack('B' * 28 * 28, fileContent[index: index + 28 * 28])
            
            # print(label_index)
            try:
                label = struct.unpack('B', labels_file_content[label_index: label_index + 1])[0]
            except:
                x = 0
                # print(label_index, len(labels_file_content))
            if bleh == False:
                print_byte_array_like_a_number(byte_array)
                net.input_image(byte_array, label)
                bleh = True

            

            label_index += 1
            index += 1
            if label_index < 15:
                print(label, end=" ")
            # print(len(byte_array))
            # print(byte_array)
            # print("---------------------------------")
                # print(fileContent)


def print_byte_array_like_a_number(row_data):
    for index, byte in enumerate(row_data):
        if index % 28 == 0:
            print("")
        if byte > 100:
            print("1", end="")
        else:
            print("0", end="")
        



load_training_binary_file()