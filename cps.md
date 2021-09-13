9/13/2021

This is my attempt to shore up some understanding on CPS. I feel that it is an 
important basic concept that I need to work on, so I am doing some work with it here.

The notes are CS6110 Spring 2013 that Professor Myers taught.

Consider the expression:
```
if x <= 0 then x else x + 1
```
which can immediately be rewritten as 
```
(if [.] then x else x + 1)[x <= 0]
```
using standard hole notation for evaluation contexts.

But the other way to write this, which is a clever observation, 
is that we can **fill-in** x<=0 as an **argument to a function**
which then rewrites it in a completely new way. Below is the function,
and note how the order is pulled inside out.

```
(\e. if e] then x else x + 1)(x <= 0)
```

A different example from CS 4110:
```
1 + (2 + (3 + 4))
```
which can be rewritten as
```
(\x. x)(1 + (2 + (3 + 4)))
```
and now we can rewrite as
```
k = \x.x
k0 = \a.k a
k1 = \b.k0 (1 + b)
k2 = \c.k1 (2 + c)
k3 = \d.k2 (3 + d)
```
And now we can evaluate 
```
k3 4
```
to get the computation.
Expanded out, it looks like
```
(\d. (\c. (\b. (\a. (\x.x) a) (1 + b)) (2 + c)) (3 + d)) 4
```
Note that the function now acts as what is to happen next, and the argument
is what happened before. Evaluation order is made explicit. The function is essentially
unraveled, with the inner most compuation occuring first.

As a simple example, we can now generalize the computation previously, to any string
of airthmetic operations.

As an aside, it becomes interesting, now, to consider translating a core subset
of scheme into continuation passing form, and then seeing how it behaves. Furthermore,
it would be nice to add in the call/cc operator to this core subset, and also
add in the backtracking operator.

Let me define the grammar:

v ::= x | \x1 ... xn.e
e ::= v0 v1 v2 ... vn

Compare this to the standard lambda calculus grammar:
v ::= \x.e 
e ::= x | e0 e1

Now we have 


