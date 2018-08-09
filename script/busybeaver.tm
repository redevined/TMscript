###
Busy beaver 3 TM
Generates six 1s on an empty tape with only three states
Run with: python -Bm src.tmscript busybeaver.tm
###

# q0
() -> (q0)
(q0, _) -> (q1, '1', R)

# q1
(q1, '1') -> (R)
(q1, _) -> (q2, R)

# q2
(q2, _) -> ('1', L)
(q2, '1') -> (q0, L)
