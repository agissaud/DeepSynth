from PIL import Image, ImageDraw
import math

IMG_WIDTH = IMG_HEIGHT = 1080
SHAPE_SCALING = 30
POSITION_SCALING = 100
ROTATION_SCALING = 36
DEFAULT_POSITION = (IMG_WIDTH/2, IMG_HEIGHT/2)
DEFAULT_OUTLINE_COLOR = "black"

listeShape = []

class Shape:
    fill_color = "black"
    position = DEFAULT_POSITION
    rotation = 0

    def __init__(self):
        listeShape.append(self)

    def draw(self, im):
        return im

    def move(self, a, b):
        # ATTENTION COORDS
        self.position = (self.position[0] + a*POSITION_SCALING, self.position[1] + b*POSITION_SCALING)

    def rotate(self, degree):
        self.rotation += degree*ROTATION_SCALING

class Polygon(Shape):
    nb_sides = 3
    scale = 1
    fill_color = "purple"

    def __init__(self, nb_sides, dimension):
        Shape.__init__(self)
        self.scale = dimension
        self.nb_sides = nb_sides if nb_sides >= 3 else 3
        # RAISE ERRORS

    def draw(self, img):
        return ImageDraw.Draw(img).regular_polygon((self.position, SHAPE_SCALING*self.scale), self.nb_sides, rotation=self.rotation, outline=DEFAULT_OUTLINE_COLOR, fill=self.fill_color)

class Rectangle(Shape):
    position2 = None
    fill_color = "red"

    def __init__(self, width, height):
        Shape.__init__(self)
        self.position2 = (self.position[0] + width*SHAPE_SCALING, self.position[1] + height*SHAPE_SCALING)

    def draw(self, img):
        return ImageDraw.Draw(img).rectangle((self.position, self.position2), outline=DEFAULT_OUTLINE_COLOR, fill=self.fill_color, width=3)

    def move(self, a, b):
        self.position = (self.position[0] + a * POSITION_SCALING, self.position[1] + b * POSITION_SCALING)
        self.position2 = (self.position2[0] + a * POSITION_SCALING, self.position2[1] + b * POSITION_SCALING)
        
'''
    def rotate(self, degree):
        # CA BUUUUUUGGG => PAS POSSIBLE A FAIRE => RAISE ERROR
        degree = degree*ROTATION_SCALING
        x0, y0 = self.position
        x1, y1 = self.position2
        distance = math.sqrt((x0-x1)**2 + (y0-y1)**2)
        arg = math.atan2(y0-y1, x0-x1)
        self.position2 = (distance * math.cos(math.radians(degree) + arg) + self.position[0], -distance * math.sin(math.radians(degree) + arg) + self.position[1])
'''

class Circle(Shape):
    radius = 0
    fill_color = "green"

    def __init__(self, radius):
        Shape.__init__(self)
        self.radius = radius*SHAPE_SCALING

    def draw(self, img):
        return ImageDraw.Draw(img).ellipse(((self.position[0] - self.radius, self.position[1] - self.radius,), (self.position[0] + self.radius, self.position[1]+ self.radius,)), outline=DEFAULT_OUTLINE_COLOR, fill=self.fill_color, width=3)

def draw_all_shape_show():
    img = Image.new("RGB", size=(IMG_WIDTH, IMG_HEIGHT), color="white")
    for s in listeShape:
        s.draw(img)
    img.show()

def draw_all_shape():
    img = Image.new("RGB", size=(IMG_WIDTH, IMG_HEIGHT), color="white")
    for s in listeShape:
        s.draw(img)
    return img

print("hello from the other shape")
eye1 = Polygon(5,3)
eye1.move(-2,-2)
eye2 = Polygon(5,3)
eye2.move(2,-2)
s4 = Circle(4)
smile1 = Rectangle(10, 3)
smile1.move(-3, 2)
smile2 = Rectangle(10, 3)
smile2.move(0, 2)
draw_all_shape_show()
