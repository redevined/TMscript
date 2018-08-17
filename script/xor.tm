###
XOR TM
This TM calculates the XOR product of two bitstrings
Input is separated by a space character
###

# skip everything until the end of the input
() -> (q0)
(q0, {'0', '1', ' ', 'e', 'n'}) -> (R)
(q0, _) -> (q1, L)

# delete lsd of second bitstring
(q1, '0') -> (r0, _, L)
(q1, '1') -> (r1, _, L)
(q1, ' ') -> (qe, _, L)

# skip forward until end of first bitstring
({r0, r1}, {'0', '1'}) -> (L)
(r0, ' ') -> (w0, L)
(r1, ' ') -> (w1, L)

# add last deleted bit and last bit of first bitstring
({w0, w1}, {'e', 'n'}) -> (L)
(w0, '0') -> (q0, 'n', R)
(w0, '1') -> (q0, 'e', R)
(w0, _) -> (q0, 'n', R)
(w1, '0') -> (q0, 'e', R)
(w1, '1') -> (q0, 'n', R)
(w1, _) -> (q0, 'e', R)

# replace e and n with 1 and 0
(qe, 'e') -> ('1', L)
(qe, 'n') -> ('0', L)
(qe, _) -> (qf)
(qf) -> ()
