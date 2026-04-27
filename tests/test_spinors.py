import numpy as np
from spinors import *

def test_pauli_matrices():
    for x in s:
        assert (np.allclose(0, x.trace()))
        assert np.allclose(x, x.conj().T)
        assert np.allclose(id, x @ x)