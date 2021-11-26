from type_system import *
from program import *
from shape import *

SHAPE = PrimitiveType('shape')
FIXED = PrimitiveType('fixed')

def _polygon(n):
    return lambda l : Polygon(n, l)

def _rectangle(width):
    return lambda height : Rectangle(width, height)

def _point(x, y):
    return 0

def _semicircle(r):
    return 0

def _circle(r):
    return Circle(r)

def _spiral(dtheta):
    return 0

def _greekSpiral(n):
    return 0

def _scurve(r):
    return 0

def _radialSymmetry(n):
    return 0

def _move(shape):
    return lambda shape: lambda x : lambda y : shape.move(x,y)

def _merge(shape):
    return lambda s1 : lambda s2 : Merge(s1, s2)

def _concat(f1):
    lambda f1 : lambda f2 : None

def _rotate(shape):
    return lambda degree : shape.rotate(degree)


semantics = {
    "circle": _circle,
    "semicircle": _semicircle,
    "spiral": _spiral,
    "greekspiral": _greekSpiral,
    "scurve": _scurve,
    "polygon": _polygon,
    "rectangle": _rectangle,
    "point": _point,
    "rsymmetry": _radialSymmetry,
    "move": _move,
    "merge": _merge,
    "fix": lambda shape: shape,
    "concat": _concat
    "rotate" : _rotate,
    "0" : 0,
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "10" : 10
}

primitive_types = {
    "circle": Arrow(INT, SHAPE),
    "semicircle": Arrow(INT, SHAPE),
    "spiral": Arrow(INT, SHAPE),
    "greekspiral": Arrow(INT, SHAPE),
    "scurve": Arrow(INT, SHAPE),
    "polygon": Arrow(INT, Arrow(INT, SHAPE)),
    "rectangle" : Arrow(INT, Arrow(INT, SHAPE)),
    "point": Arrow(INT, Arrow(INT, POINT)),
    "rsymmetry": Arrow(INT, Arrow(SHAPE, SHAPE)),
    "move": Arrow(SHAPE, Arrow(INT, Arrow(INT, SHAPE))),
    "merge": Arrow(SHAPE, Arrow(SHAPE, SHAPE)),
    "fix": Arrow(SHAPE, FIXED)
    "concat": Arrow(FIXED, Arrow(FIXED, FIXED))
    "rotate": Arrow(SHAPE, Arrow(INT, SHAPE)),
    "0" : INT,
    "1" : INT,
    "2" : INT,
    "3" : INT,
    "4" : INT,
    "5" : INT,
    "6" : INT,
    "7" : INT,
    "8" : INT,
    "9" : INT,
    "10" : INT
}