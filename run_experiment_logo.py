from experiment_helper_logo import *
from shape import *

print("hello from the other shape")
eye1 = Polygon(5,3)
eye1.move(-2,-2)
eye2 = Polygon(5,3)
eye2.move(2,-2)
s4 = Circle(4)
s5 = Circle(4)
smile1 = Rectangle(10, 3)
smile1.move(-3, 2)
smile2 = Rectangle(10, 3)
smile2.move(0, 2)

merged = Merge(eye1, eye2)
merged.move(-1,-1)
draw_all_shape_show()

loss_function_logo(listeShape)