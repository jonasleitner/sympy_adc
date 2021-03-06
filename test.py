import numpy as np
from sympy import KroneckerDelta, symbols, latex, Dummy, Rational, Add, Mul, S, Pow
from sympy.core.function import diff
from sympy.physics.secondquant import AntiSymmetricTensor, contraction, substitute_dummies, wicks, NO, Fd, F, evaluate_deltas, Dagger
from itertools import combinations

from indices import assign_index, make_pretty, pretty_indices, indices, get_first_missing_index
from groundstate import ground_state, Hamiltonian
from isr import gen_order_S, intermediate_states
from properties import properties
from secular_matrix import secular_matrix
from transformexpr import make_canonical, make_real, change_tensor_name, filter_tensor, remove_tensor, simplify, sort_by_n_deltas, sort_by_type_deltas, sort_by_type_tensor, sort_tensor_contracted_indices
from misc import cached_member, transform_to_tuple

# i, j, k, l, m, n, o = symbols('i,j,k,l,m,n,o', below_fermi=True, cls=Dummy)
# a, b, c, d, e, f, g = symbols('a,b,c,d,e,f,g', above_fermi=True, cls=Dummy)
# p, q, r, s = symbols('p,q,r,s', cls=Dummy)

h = Hamiltonian()
mp = ground_state(h, first_order_singles=False)
isr = intermediate_states(mp, variant="pp")
m = secular_matrix(isr)
op = properties(isr)

bla = m.mvp_block_order(2, "ph", "ph,ph", indices="ia")
print(latex(bla))
bla = mp.indices.substitute_indices(bla)
# bla = change_tensor_name(bla, "X", "Ycc")
print()
bla = simplify(bla, True)
print(latex(bla))
sort = sort_tensor_contracted_indices(bla, "Y")
print("Non Canonical result:\n\n")
for t, expr in sort.items():
    print(f"{len(expr.args)} terms with sum {t}:\n{latex(expr)}\n\n")

bla = make_canonical(bla, True)
sort = sort_tensor_contracted_indices(bla, "Y")
print("Canonical result:\n\n")
for t, expr in sort.items():
    print(f"{len(expr.args)} terms with sum {t}:\n{latex(expr)}\n\n")
