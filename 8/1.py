

def get_layers(data, layersize):
    num_layers = int(len(data) / layersize)
    layers = []
    for i in range(num_layers):
        layers.append(data[i * layersize:(i+1)*layersize])
    return layers

def get_count_of_value(layer, value):
    return layer.count(value)

with open("input", "r") as f:
    data = f.read().strip()


width = 25
height = 6
pixels_in_layer = width * height

layers = get_layers(data, pixels_in_layer)
num_zeros = []
for l in layers:
    num_zeros.append(get_count_of_value(l, '0'))
ordered = sorted(num_zeros)
min_ind = num_zeros.index(ordered[0])
print(get_count_of_value(layers[min_ind], '1') * get_count_of_value(layers[min_ind], '2'))



