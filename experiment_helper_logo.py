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

def make_program_checker_logo(dsl: DSL, examples) -> Callable[[Program, bool], bool]:
    def checker(prog: Program, use_cached_evaluator: bool) -> bool:
        if use_cached_evaluator:
            for i, example in enumerate(examples):
                input, output = example
                prog.eval(dsl, input, i)
                out = draw_all_shape()
                if output != out:
                    return False
                listeShape = []
            return True
        else:
            for example in examples:
                input, output = example
                prog.eval(dsl, input, i)
                out = draw_all_shape()
                if output != out:
                    return False
                listeShape = []
            return True
    return checker