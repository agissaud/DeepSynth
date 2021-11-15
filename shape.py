from PIL import Image, ImageDraw

IMG_WIDTH = IMG_HEIGHT = 1080
SHAPE_SCALING = 40
DEFAULT_POSITION = (IMG_WIDTH/2, IMG_HEIGHT/2)

liste

class Shape:
    scale = 1
    fill_color = "black"
    im

    def __init__(self, dimension):
        self.scale = dimension

    def draw(self, im):
        return im

class Polygon(Shape):
    nb_sides = 3

    def __init__(self, nb_sides, dimension,):
        self.scale = dimension
        self.nb_sides = nb_sides if nb_sides >= 3 else 3

    def draw(self, im):
        return im.regular_polygon((DEFAULT_POSITION, SHAPE_SCALING*self.scale), self.nb_sides, fill=self.fill_color)