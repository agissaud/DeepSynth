import torch
from type_system import INT, STRING, Arrow, Type
import type_system
from Predictions.models import RulesPredictor, BigramsPredictor
from pcfg import PCFG
from typing import Callable, List, Tuple
from dsl import DSL
from program import Program
import experiment_helper
import shape as sh

PENALITY_OUT_OF_BOUND = 5
PENALITY_SUPERPOSITION = 5

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
        if 0 <= s.position[0] <= sh.IMG_WIDTH and 0 <= s.position[1] <= sh.IMG_HEIGHT:
            listShapeIn.append(s)
        else:
            score += PENALITY_OUT_OF_BOUND

    # Superposé parfaitement
    for i, s in enumerate(listShapeIn):
        for s2 in listShapeIn[(i+1):]:
            if s == s2 :
                score += PENALITY_SUPERPOSITION

    return (valid, score)