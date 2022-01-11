from PIL import Image, ImageDraw
import math

# Image parameters
IMG_WIDTH = IMG_HEIGHT = 1080
SHAPE_SCALING = 30
POSITION_SCALING = 100
ROTATION_SCALING = 36
DEFAULT_POSITION = (IMG_WIDTH/2, IMG_HEIGHT/2)
DEFAULT_OUTLINE_COLOR = "black"

#Intern representation
listeShape = []
start_color = [1, 0, 0]

def get_list_shape():
    global listeShape
    return listeShape

def next_color():
    global start_color
    for i in range(3):
        if start_color[i] < 255:
            start_color[i] += 1
            return True
    return False

def get_fill_color():
    return tuple(start_color)

class Shape:
    fill_color = "orange"
    fill_color_colision = None
    position = DEFAULT_POSITION
    rotation = 0

    def __init__(self):
        listeShape.append(self)
        self.fill_color_colision = get_fill_color()
        next_color()

    def draw(self, im, collision=False):
        return im

    def move(self, a, b):
        self.position = (self.position[0] + a*POSITION_SCALING, self.position[1] + b*POSITION_SCALING)
        return self

    def rotate(self, degree):
        self.rotation += degree*ROTATION_SCALING
        return self

    def get_representative_points(self):
        return [self.position]

    def point_in_shape(self, point):
        return point == self.position

    def is_superposed_on(self, shape):
        for point in shape.get_representative_points():
            if not self.point_in_shape(point):
                return False
        return True


class Polygon(Shape):
    nb_sides = 3
    scale = 1
    fill_color = "purple"

    def __init__(self, nb_sides, dimension):
        Shape.__init__(self)
        self.scale = dimension if dimension > 0 else 1
        self.nb_sides = nb_sides if nb_sides >= 3 else 3
        # RAISE ERRORS

    def draw(self, img, collision=False):
        c = self.fill_color_colision if collision else self.fill_color
        return ImageDraw.Draw(img).regular_polygon((self.position, SHAPE_SCALING*self.scale), self.nb_sides, rotation=self.rotation, outline=DEFAULT_OUTLINE_COLOR, fill=c)

    def __eq__(self, other):
        if type(other).__name__ == type(self).__name__:
            return self.position == other.position and self.nb_sides == other.nb_sides \
            and self.scale == other.scale and self.rotation == other.rotation
        return False


class Rectangle(Shape):
    position2 = None
    fill_color = "red"

    def __init__(self, width, height):
        Shape.__init__(self)
        self.position2 = (self.position[0] + width*SHAPE_SCALING/2, self.position[1] + height*SHAPE_SCALING/2)
        self.position = (self.position[0] - width*SHAPE_SCALING/2, self.position[1] - height*SHAPE_SCALING/2)

    def draw(self, img, collision=False):
        c = self.fill_color_colision if collision else self.fill_color
        return ImageDraw.Draw(img).rectangle((self.position, self.position2), outline=DEFAULT_OUTLINE_COLOR, fill=c, width=3)

    def move(self, a, b):
        self.position = (self.position[0] + a * POSITION_SCALING, self.position[1] + b * POSITION_SCALING)
        self.position2 = (self.position2[0] + a * POSITION_SCALING, self.position2[1] + b * POSITION_SCALING)
        return self

    def __eq__(self, other):
        if type(other).__name__ == type(self).__name__:
            return self.position == other.position and self.position2 == other.position2
        return False

    def get_representative_points(self):
        list = Shape.get_representative_points(self)
        list.append(self.position)
        list.append(self.position2)
        list.append((self.position2[0], self.position[1]))
        list.append((self.position[0], self.position2[1]))
        return list

    def point_in_shape(self, point):
        return self.position[0] <= point[0] <= self.position2[0] and self.position[1] <= point[1] <= self.position2[1]

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

    def draw(self, img, collision=False):
        c = self.fill_color_colision if collision else self.fill_color
        return ImageDraw.Draw(img).ellipse(((self.position[0] - self.radius, self.position[1] - self.radius,), (self.position[0] + self.radius, self.position[1]+ self.radius,)), outline=DEFAULT_OUTLINE_COLOR, fill=c, width=3)

    def __eq__(self, other):
        if type(other).__name__ == type(self).__name__:
            return self.position == other.position and self.radius == other.radius
        return False

class Merge(Shape):
    shapes = []

    def __init__(self, s1, s2):
        self.shapes.append(s1)
        self.shapes.append(s2)

    def draw(self, im, collision=False):
        for s in self.shapes:
            s.draw(im, collision)
        return im

    def move(self, a, b):
        # ATTENTION COORDS
        for s in self.shapes:
            s.move(a, b)
        return self

    def rotate(self, degree):
        for s in self.shapes:
            s.rotate(degree)
        return self

    def get_representative_points(self):
        l = []
        for s in self.shapes:
            l.extend(s.get_representative_points())
        return l

    def point_in_shape(self, point):
        for s in self.shapes:
            if s.point_in_shape(point):
                return True
        return False

def draw_all_shape_show():
    img = Image.new("RGB", size=(IMG_WIDTH, IMG_HEIGHT), color="white")
    for s in listeShape:
        s.draw(img)
    img.show()

def draw_all_shape_to_img(lShape=listeShape, collision=False):
    img = Image.new("RGB", size=(IMG_WIDTH, IMG_HEIGHT), color="white")
    for s in lShape:
        s.draw(img, collision=collision)
    return img

def clear_list_shape():
    global listeShape
    listeShape = []

def print_list_shape():
    global listeShape
    print(listeShape)