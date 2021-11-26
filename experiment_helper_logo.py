import torch
from type_system import INT, STRING, Arrow, Type
import type_system
from Predictions.models import RulesPredictor, BigramsPredictor
from pcfg import PCFG
from typing import Callable, List, Tuple
from dsl import DSL
from program import Program
import experiment_helper
import shape

COEF_OUT_OF_BOUND = 5
COEF_SUPERPOSITION = 5

def make_program_checker_logo(dsl: DSL, examples) -> Callable[[Program, bool], bool]:
    def checker(prog: Program, use_cached_evaluator: bool) -> bool:
        if use_cached_evaluator:
            for i, example in enumerate(examples):
                input, output = example
                prog.eval(dsl, input, i)
                out = draw_all_shape() # Récupérer l'image
                if output != out:
                    return False
                clear_list_shape()
            return True
        else:
            for example in examples:
                input, output = example
                prog.eval(dsl, input, i)
                out = draw_all_shape()
                if output != out:
                    return False
                clear_list_shape()
            return True
    return checker

def loss_function_logo(listOfShape):
    valid = True
    score = 0

    if listOfShape == []:
        valid = False

    listShapeIn = []
    # En dehors du canvas
    for s in listOfShape:
        if 0 <= s.position[0] <= IMG_WIDTH and 0 <= s.position[1] <= IMG_HEIGHT:
            listShapeIn.append(s)
        else:
            score += PENALITY_OUT_OF_BOUND

    # Superposé parfaitement
    for s in listShapeIn:
        print(type(s).__name__)
        for s2 in listShapeIn:
            if s == s2 and s is not s2:
                print("aled")

    return (valid, score)