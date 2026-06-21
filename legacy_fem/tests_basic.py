import pytest
import os
from fem_object import TObject

MESH_PATH = os.path.join(os.path.dirname(__file__), 'mesh', 'cube.trpa')

def test_cube_setup():
    obj = TObject()
    assert obj.set_mesh(MESH_PATH) == True

def test_cube_solve():
    obj = TObject()
    e = [2.0E+11]
    m = [0.3]
    assert obj.set_mesh(MESH_PATH) == True
    obj.set_problem_type('static')
    obj.set_solve_method('direct')
    obj.set_elasticity(e, m)
    obj.add_boundary_condition('0', 'z=0', 1 | 2 | 4)
    obj.add_surface_load('1.0E+8', 'z=1', 4)
    assert obj.calc() == True
