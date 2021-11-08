from type_system import *
from program import *
import math

# OPTION 1
FLOAT = PrimitiveType('float')
POINT = PrimitiveType('point')

# OPTION 2
SHAPE = PrimitiveType('shape')

''' Renvoie une liste de positions (pour dessiner les sommets des polygones) selon le nombre de sommets n'''
def _listPosition(n):

def drawPoly(n, l):
    # DRAW ICI

def _polygone(n):
    return lambda l : drawPoly(n, l)
    #dessiner polygone a n cotés au centre

def _point(x, y):

def _semicircle(r):

def _circle(r):

def _spiral(dtheta):

def _greekSpiral(n):

def _scurve(r):

def _reproduceShape(n, shape):
    for pos in _listPosition(n):
        draw(pos, shape) # PSEUDO CODE

def _radialSymmetry(n):
    return lambda shape: _reproduceShape(n, shape)

def _move(x, y, shape):

def _merge(shape):
    return lambda s1 : lambda s2 : merge(s1, s2)

def _rotate(degree):
    return lambda s: _rotateShape(degree, s)

def _rotateShape(degree, shape):
    # rotate shape

semantics = {
    "circle": _circle,
    "semicircle": _semicircle,
    "spiral": _spiral,
    "greekspiral": _greekSpiral,
    "scurve": _scure,
    "polygone": _polygone,
    "point": _point,
    "rsymmetry": _radialSymmetry,
    "move": _move,
    "merge": _merge,
    "rotate" : _rotate
}

primitive_types = {
    "circle": Arrow(FLOAT, SHAPE),
    "semicircle": Arrow(FLOAT, SHAPE),
    "spiral": Arrow(FLOAT, SHAPE),
    "greekspiral": Arrow(INT, SHAPE),
    "scurve": Arrow(FLOAT, SHAPE),
    "polygone": Arrow(INT, Arrow(FLOAT, SHAPE)),
    "point": Arrow(FLOAT, Arrow(FLOAT, POINT)),
    "rsymmetry": Arrow(INT, Arrow(SHAPE, SHAPE)),
    "move": Arrow(FLOAT, Arrow(FLOAT, SHAPE)),
    "merge": Arrow(SHAPE, Arrow(SHAPE, SHAPE))
}