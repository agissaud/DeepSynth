from type_system import *
from program import *
from shape import *

SHAPE = PrimitiveType('shape')
FIXED = PrimitiveType('fixed')


def _polygon(n):
    return lambda l: Polygon(n, l)


def _rectangle(width):
    return lambda height: Rectangle(width, height)


def _circle(r):
    return Circle(r)


def _move(shape):
    return lambda x: lambda y: shape.move(x, y)


def _merge():
    return lambda s1: lambda s2: Merge(s1, s2)


def _concat(f1):
    return lambda f2: None


def _rotate(shape):
    return lambda degree: shape.rotate(degree)


semantics = {
    "circle": _circle,
    "polygon": _polygon,
    "rectangle": _rectangle,
    "move": _move,
    "merge": _merge,
    "fix": lambda shape: shape,
    "concat": _concat,
    "rotate": _rotate,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10
}

primitive_types = {
    "circle": Arrow(INT, SHAPE),
    "polygon": Arrow(INT, Arrow(INT, SHAPE)),
    "rectangle": Arrow(INT, Arrow(INT, SHAPE)),
    "move": Arrow(SHAPE, Arrow(INT, Arrow(INT, SHAPE))),
    "merge": Arrow(SHAPE, Arrow(SHAPE, SHAPE)),
    "fix": Arrow(SHAPE, FIXED),
    "concat": Arrow(FIXED, Arrow(FIXED, FIXED)),
    "rotate": Arrow(SHAPE, Arrow(INT, SHAPE)),
    "0": INT,
    "1": INT,
    "2": INT,
    "3": INT,
    "4": INT,
    "5": INT,
    "6": INT,
    "7": INT,
    "8": INT,
    "9": INT,
    "10": INT
}
