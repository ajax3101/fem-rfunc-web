import numpy as np

def r_and(x, y):
    """
    Rvachev R-conjunction (intersection)
    R(x, y) = x + y - sqrt(x^2 + y^2)
    """
    return x + y - np.sqrt(x**2 + y**2)

def r_or(x, y):
    """
    Rvachev R-disjunction (union)
    R(x, y) = x + y + sqrt(x^2 + y^2)
    """
    return x + y + np.sqrt(x**2 + y**2)

def r_and_n(*args):
    """
    Generalized R-conjunction for n arguments
    R(x1, x2, ..., xn) = sum(xi) - sqrt(sum(xi^2))
    Note: The specific C++ code does W1 + W2 + W3 - sqrt(W1^2 + W2^2 + W3^2)
    """
    args = np.array(args)
    return np.sum(args, axis=0) - np.sqrt(np.sum(args**2, axis=0))

def rfunc(x, y):
    """
    The specific R-function implemented in Main.cpp.
    It constructs a domain from primitive circular domains.
    """
    R = 0.4
    R1 = 0.25

    W1 = -(R1**2 - (x - 0.6)**2 - y**2)
    W2 = -(R**2 - x**2 - y**2)
    W3 = -(R1**2 - (x + 0.6)**2 - y**2)

    # W1 + W3 + W2 - sqrt(W1^2 + W2^2 + W3^2)
    # Note: using numpy arrays natively supports scalar and vectorized evaluation.
    return W1 + W3 + W2 - np.sqrt(W1**2 + W2**2 + W3**2)

def sign(val):
    """Sign function mimicking the C++ logic: 1 if >0, -1 if <0, 0 if ==0"""
    return np.sign(val)

def get_rfunc_coordinate(cx, cy, fi, radius, eps=0.0001):
    """
    Bisection algorithm to find the intersection of the R-function boundary
    and a ray originating at (cx, cy) with angle fi and maximum length radius.

    Returns (True, ResX, ResY) if an intersection is found.
    Returns (False, 0.0, 0.0) if no boundary is intersected in the given radius.
    """
    r1 = 0.0
    r2 = radius

    x1 = r1 * np.cos(fi) + cx
    y1 = r1 * np.sin(fi) + cy
    x2 = r2 * np.cos(fi) + cx
    y2 = r2 * np.sin(fi) + cy

    s1 = sign(rfunc(x1, y1))
    s2 = sign(rfunc(x2, y2))

    if s1 == s2:
        return False, 0.0, 0.0

    tx, ty = 0.0, 0.0
    while True:
        r = (r1 + r2) * 0.5
        tx = r * np.cos(fi) + cx
        ty = r * np.sin(fi) + cy
        ts = sign(rfunc(tx, ty))

        if ts == s1:
            r1 = r
        else:
            r2 = r

        if np.abs(rfunc(tx, ty)) <= eps:
            break

    return True, float(tx), float(ty)
