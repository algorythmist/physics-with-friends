import numpy as np
from sympy import symbols, Matrix, exp, I

def commutator(a,b):
    return a@b - b@a

def anticommutator(a,b):
    return a @ b + b @ a

def to_pauli_vector(vector):
    assert len(vector) == 3
    return np.tensordot(vector, s, axes=1)


id = np.identity(2)
s1 = np.array([[0, 1], [1, 0]])
s2 = np.array([[0, -1j], [1j, 0]])
s3 = np.array([[1, 0], [0, -1]])

s = np.array([s1, s2, s3])



if __name__ == "__main__":
    x = np.array([1,1,1])
    print(to_pauli_vector(x))

    t = symbols('t')
    M = Matrix(s2)
    result = exp(I * t * M)
    print(result)
