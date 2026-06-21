import pytest
import numpy as np
from rfunc_core import r_and, r_or, r_and_n, rfunc, get_rfunc_coordinate, sign

def test_r_and_scalar():
    assert np.isclose(r_and(1, 0), 0.0)
    assert np.isclose(r_and(1, 1), 2 - np.sqrt(2))

def test_r_and_vectorized():
    x = np.array([1, 1, -1])
    y = np.array([0, 1, -1])
    expected = np.array([0, 2 - np.sqrt(2), -2 - np.sqrt(2)])
    np.testing.assert_allclose(r_and(x, y), expected)

def test_r_or_scalar():
    assert np.isclose(r_or(1, 0), 2.0)
    assert np.isclose(r_or(1, 1), 2 + np.sqrt(2))

def test_rfunc_domain_signs():
    far_val = rfunc(10, 10)
    assert far_val > 0

    center_val = rfunc(0, 0)
    assert center_val < 0

def test_get_rfunc_coordinate():
    # The actual geometric intersection in the combined R-function is slightly different from just R=0.4
    # Because the W1, W3 terms influence the root smoothly
    # We'll assert it finds *A* valid root that resolves the rfunc to 0.
    success, res_x, res_y = get_rfunc_coordinate(0, 0, 0, 2.0, eps=1e-5)

    assert success is True
    # The root should be around 0.448 based on debug output
    assert np.isclose(res_x, 0.448, atol=1e-2)
    assert np.isclose(res_y, 0.0, atol=1e-2)

    val_at_root = rfunc(res_x, res_y)
    assert np.abs(val_at_root) <= 1e-4

def test_get_rfunc_coordinate_no_hit():
    success, res_x, res_y = get_rfunc_coordinate(0, 0, 0, 0.1)
    assert success is False
    assert res_x == 0.0
    assert res_y == 0.0
