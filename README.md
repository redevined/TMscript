Concept for TMscript
====================

A TMscript script describes a (non-)deterministic Turing machine.
It receives a string as input and outputs a new string, created through application of the TM on the input.
Turing machine acceptors can also be modeled, to check whether the input is part of the language defined by the given TM.
If executed with the -a or --accept flag, TMscript returns 1 if the input is accepted, 0 otherwise.
You can read about Turing machines on [Wikipedia](https://en.wikipedia.org/wiki/Turing_machine "Yeah, I know what you guys are thinking about Wikipedia articles...").

> Important note: Non-deterministic behavior is not yet implemented.
> Therefore features like multiple output states and epsilon transitions might not work right now.

### Example usage:

	tmscript machine.tm hello
	> world

	tmscript acceptor.tm -a hello
	> 1

## Language features:

### Transitions

A TMscript code consists of multiple state transition definitions.
The set of states, or the alphabet are implicitly derived from the given declarations.
Definitions can be in any order.
The definition template looks like this:

	(q, a) -> (q', a', M)

q and q' are states, a and a' symbols from the alphabet and M is one of L, N, R.
If q is not present in the definition, the transition is duplicated for each state, on the other hand if a is not present, the transition can be applied for any symbol.
q and a can also be sets of states/symbols, in fact, a single q is interpreted as {q}.

	({q, p}, a) -> (q', a', M)
	# equals (q, a) -> (q', a', M)   (p, a) -> (q', a', M)

	(q, {a, b}) -> (q', a', M)
	(a) -> (q', a', M)
	(q) -> (q', a', M)

Using sets or leaving out literals on the right side of the declaration works a little bit different.
If a transition to a set of states happens, the TM transitions into all of the states at the same time (non-deterministic behavior).

	(q, a) -> ({q', p'}, a', M)
	# equals (q, a) -> (q', a', M)   (q, a) -> (p', a', M)

	(q, a) -> (q', {a', b'}, M)
	(q, a) -> (q', a', {L, R})

Leaving out q' is equal to not changing the state with the transition, as is for a' and the current symbol.
Also, omitting the movement direction M is equal to no movement N.

	(q, a) -> (a', M)
	# equals (q, a) -> (q, a', M)

	(q, a) -> (q', M)
	(q, a) -> (q', a')

To define a starting state, you can leave the left side of the declaration empty.
There can only be one starting state.

	() -> (q')

If you need accepting states, just omit any literals on the right side.
The TM will stop once it reaches an accepting state.

	(q) -> ()
	({q, p}) -> ()

Use # for line comments and ### for block comments.

	# This is a comment
	###
	And this a block comment
	###

### Identifiers and symbols:

In TMscript, states are identifiers starting with a non-number.
A symbol is a string with length one, special characters like \n or \t are allowed as well.
A movement is one of L, N, R.
Therefore a real transition would look like this:

	(q0, '0') -> (q1, '1', R)

To handle blanks, e.g. to detect the end of the input, use the constant \_.

	(q1, _) -> (q0, _, L)

Epsilon transitions are possible by using the constant eps.

	(q0, eps) -> (q1, '1', N)

However, be careful with epsilon transitions!
A TM must not contain an epsilon loop, since it would lead to infinite possible configurations.
Therefore following declarations are not allowed:

	(q0, eps) -> (q0)
	(q0, eps) -> (q1)   (q1, eps) -> (q0)
	(eps) -> (q0)
