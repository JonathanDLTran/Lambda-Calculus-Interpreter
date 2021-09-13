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
which then rewrites it in a completely new way. 

A different example of my own:
```
let x = 3 in 
let y = 5 in 
let z = 6 in
x + y + z
```
which can be rewritten as
```


Note that the function now acts as what is to happen next, and the argument
is what happened before. Evaluation order is made explicit. 

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


