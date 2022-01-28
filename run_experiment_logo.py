from experiment_helper_logo import *
from shape import *
import dsl
from DSL import logo

def print_clown():
    eye1 = Polygon(5,3)
    eye1.move(-2,-2)
    eye2 = Polygon(5,3)
    eye2.move(2,-2)
    s4 = Circle(4)
    smile1 = Rectangle(10, 3)
    smile1.move(-1, 2)
    smile2 = Rectangle(10, 3)
    smile2.move(1, 2)

    draw_all_shape_show()

def test_Rectangle_superposed():
    print("Test Rectangle masked")
    clear_list_shape()
    rec3 = Rectangle(9, 3)
    rec1 = Rectangle(8, 8)
    rec2 = Rectangle(5, 5)
    test = Polygon(10, 8)
    print("This should print True : " + str(rec1.is_superposed_on(rec2)))
    print("This should print False : " + str(rec2.is_superposed_on(rec1)))
    print("This should print False : " + str(rec3.is_superposed_on(rec1)))
    print("This should print False : " + str(rec3.is_superposed_on(rec2)))
    draw_all_shape_show()

def test_superposed_img_detection():
    print("Shape detection test")
    clear_list_shape()
    rec1 = Rectangle(8, 8)
    rec2 = Rectangle(5, 5)
    test = Polygon(10, 4)
    test.move(3, -2)
    ls = get_list_shape()
    print("This should be 0: " + str(evaluate_superposition_img(ls)))
    draw_all_shape_show()

def test_color_next():
    global start_color
    start_color = [1, 0, 0]
    print("Start color test")
    print(start_color)
    next_color()
    print(start_color)
    for i in range(254):
        next_color()
    print(start_color)
    c = (start_color)
    print(tuple(c))
    start_color = [1, 0, 0]

##############################################################

max_program_depth = 15

logoDSL = dsl.DSL(logo.semantics, logo.primitive_types)
type_request = logo.FIXED
logo_cfg = logoDSL.DSL_to_CFG(type_request, max_program_depth=max_program_depth)
logo_pcfg = logo_cfg.CFG_to_Uniform_PCFG()

generator = logo_pcfg.sampling(seed=5)

selection_loop = False

for i in range(5):
    clear_list_shape()
    a = generator.__next__()
    a.eval_naive(logoDSL, None)
    ls = get_list_shape()

    if selection_loop:
        while evaluate_superposition_img(ls) != 0 or len(ls) <= 2:
            clear_list_shape()
            a = generator.__next__()
            a.eval_naive(logoDSL, None)
            ls = get_list_shape()

    print(a)
    print("\n")
    draw_all_shape_show()
