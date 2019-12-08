class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = '2'*(width*height)

    def __str__(self):

        blockchar = '█'
        transparent = ' '
        black = '\033[94m' + blockchar + '\033[0m'
        white = '\033[92m' + blockchar + '\033[0m'

        out = ''
        for line in range(self.height):
            for pix in range(self.width):
                if self.pixels[line*width + pix] == '2':
                    out += transparent
                if self.pixels[line*width + pix] == '1':
                    out += black
                if self.pixels[line*width + pix] == '0':
                    out += white
            out += "\n"
        return(out)





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
image = Image(width, height)
for l in layers:
    for i, pixel in enumerate(l):
        if image.pixels[i] == '2':
            image.pixels = image.pixels[:i] + pixel + image.pixels[i+1:]


print(image)



