# Introduction

This is my attempt to shore up some understanding on CPS. I feel that it is an 
important basic concept that I need to work on, so I am doing some work with it here.

The notes are CS6110 Spring 2013 that Professor Myers taught, as well as CS 4110.

## Content

### Motivation for Continuation Passing Form

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
of arithmetic operations. For instance, for any string of arithmetic operations and values,
we can translate it as:
```
k = \x.x
k0 = \a.k a
k1 = \b.k0 (...)
k2 = \c.k1 (...)
k3 = \d.k2 (...)
....
```
And quite obviously the pattern generalizes.
With assignment, one can also pass not just the value but also a context as well.
We define a translation for statement level CPS and also expression level CPS.
At the statement level, CPS passes around a context as a value. At the expression level,
CPS passes around a value. 
So for example
```
let x = 3
let y = 4
x + y
```
becomes
```
k0 = \c0.c0
ke = \v c k. k (v + c1[y])
k1 = \c1 k0. k0 (ke c1[x] c1 \x.x)
k2 = \c2 k1. k1 (c2[y] = 4; c2)
k3 = \c3 k2. k2 (c3[x] = 3; c3)
```
assuming assignment generates the same context. Then the computation can be kickstarted
by calling k3 on an empty context. Note that ke is then the expression translated
as a separate part of the computation and embedded into k1.

As an aside, it becomes interesting, now, to consider translating a core subset
of scheme into continuation passing form, and then seeing how it behaves. Furthermore,
it would be nice to add in the call/cc operator to this core subset, and also
add in the backtracking operator.

We start this journey by understanding CPS via translations from the lambda calculus.

### Translating Simple Expressions to CPS

To get a hang with using CPS, let's try translating simple expressions
in direct style to CPS. 

For instance, consider an integer value ```v```. What is its CPS translation?
It should just be ```k v```, for the value has no computation in it, so instead
of "returning" the value, we send it off to the continuation. In fact, we can generalize,
and see that for any value, no computation is needed, so we can just let the continuation
use it. 

Now let's consider 2 integer expressions being added together: ```e0 + e1```.
The translation of this to CPS should preserve the following order of evaluation:
evaluate e0 to a value v0, evaluate e1 to a value v1, then add v0 and v1 together 
to get v, and finally apply k to v.

We can incrementally develop a translation for this addition expression. Define
```[[e]] k``` to be a translation of e that accepts a continuation k to be applied
on e, after e's value is computed to a value. In other words, ```[[e]] = \k. ...```. 

Since we want e0 to evaluate first, consider ```[[e0]]```, which is a function that
takes in a continuation k. What is the continuation? Well, naturally, it should take in 
the value v0, which is what e0 reduces to. Next, according to our ordering we compute
e1, so the function's body should begin by evaluating ```[[e1]]```. Finally, ```[[e1]]``
needs a continuation. This continuation takes the value v1, and adds it with v0, with the sum called v. Then it dumps v in k.

This is what the translation looks like:
```[[e0 + e1]] k = [[e0]] (\v0. [[e1]] (\v1. k (v0 + v1)))```

Not very compact. But easy to understand what is happening. CPS tells us to:

1. Compute e0 to a value v0.
2. Compute e1 to a value v1
3. Add v0 and v1 to get v
4. Do not return v, but instead let k take v.

The translation is simple, concise and intuitively makes sense. 

In general, for CPS translation, keep the high level idea of what a continuation is.
The continuation is a function that represents what will happen next, after your 
current expression is computed down to a value.

### A Few Key Points About CPS

In CPS, one question one might have is when should we have 
```[[e]] k``` versus ```k [[e]]```.

The answer is you should use ```[[e]] k```  to intuitively represent the idea of 
calculate e to a value v, then apply k after. This works when e is not yet a value.

```k [[e]]``` on the other hand represents the idea that e is really a value v, and 
we should just let k take the value v. A better way of putting this is that 
```k [[e]]``` never should occur, instead only ```k v``` is legal.

### Translating Recursive Functions to CPS

Here's an example of CPS and recursion.
Consider the length function for a list in OCaml.
```
let rec length lst = 
    match lst with 
    | [] -> 0 
    | _ :: t -> 1 + length t
```
To put this in CPS form is not so simple.
As a first try, we can do
```
let rec length lst k = 
    match lst with 
    | [] -> k 0 
    | _ :: t -> k (1 + length t k)
```
But this cannot be correct. For instance, suppose the continuation was 
not the trivial identity function, and say it was the function ```(fun x -> x + 2)```.
Clearly, the length is now going to be overinflated to be 3 times the actual
length of the list. A problem is that we don't want the continuation to be applied
at every step of recursion, only after the recursion has terminated.
Here's another try with that in mind. 
```
let rec length lst k = 
    match lst with 
    | [] -> k 0 
    | _ :: t -> (1 + length t k)
```
This time around, we still get the wrong the wrong answer when the contination is 
the function ```(fun x -> x + 2)```. Now the problem is that we want the continuation to 
still apply to the end of of recursion for non-zero length lists, not just at the end of the empty list. In other words, we want it to be applied at the end of the computation even if the list is of non-zero length. A complicating factor is that we still 
want the continuation to be applied at the base case, **if** the list is of zero length.
This somehow suggests that the continuation will be changing at every part of the 
recursion. We can use these thoughts to suggest a third version of the computation:
```
let rec length lst k = 
    match lst with 
    | [] -> k 0 
    | _ :: t -> length t (fun len -> k (1 + len))
```
Let's consider this version more closely. First, we only apply the continuation 
at the base case. This is good because we only want the continuation to be applied once,
when the recursion terminates. 

Next, notice that the continuation is now tucked away in the correct position,
so that it is applied at the end of computations for both empty and non-empty lists.

Finally, we see that the continuation changes to grow larger and larger the longer
the list is and the more recursion is needed.

Indeed, this ends up being a correct translation of the length function to CPS form. 

To try an example, we see:
```
length [0; 1] (fun x -> x)
-> length [1] (fun len -> (fun x -> x) (1 + len))
-> length [] (fun len -> (fun len -> (fun x -> x) (1 + len)) (1 + len))
-> (fun len -> (fun len -> (fun x -> x) (1 + len)) (1 + len)) 0 
-> (fun len -> (fun x -> x) (1 + len)) (1 + 0)
-> (fun len -> (fun x -> x) (1 + len)) 1
-> (fun x -> x) (1 + 1)
-> (fun x -> x) 2
-> 2
```
Which is the correct result!

This ultimately suggests a new interpretation in the translation of CPS
for recursive functions:
In the recursive call, we have ```len t (fun len -> k (1 + len))```.
Our new continuation ```(fun len -> k (1 + len))``` represents what happens 
to the value of ``len t``. Intuitively, this says, calculate length of t, 
then apply ```(fun len -> k (1 + len))``` to the calculated length, 
which is exactly as we want, because the continuation first adds 1 to the length,
getting the length of the whole list, then applies k to it, which is as the continuation 
k should be used.

Here's another way to read into a recursive function in cps:
```f x k```
means intuitively calculate f on x recursively in the normal sense, ignoring 
all CPS. Then apply k to this recusive calculation. Now it makes absoluate sense
why the recusive case is written ```len t (fun len -> k (1 + len))```.
This is precisly because we calculate ```len t```, ignoring CPS, then we apply the 
continuation adding 1 to it, and then apply k. The new continuation captures what 
we should do at the end, and the end is at the bottom of the stack, where we apply
k to 0.

Let us consider another explanation. The continuation represents the computation 
**after** the current computation, which in our case, is the recursive function.

Hence, we should be applying the computation after adding 1 to length t. But this
would mean we should not apply the continuation to the base case. To avoid this issue,
we instead move the add 1 to length into the continuation itself, allowing us to 
apply the continuation in the base case.

And a related observation: Notice that in CPS recursion, we only go down the stack,
never up. Because going up means we return back to the caller, which is antithecal
to CPS. Rather than returning, we call something else: the continuation, which represents
the unwinding of the stack!!

We can easily generalize the above procedure to maps, folds, and other recursive
functions. The above even works for mutual recursion.

Here's an example of converting mutual recursion to CPS:
The pre-CPS version is shown here.
```
let rec even n = 
    if n = 0 then true 
    else odd (n - 1)

let rec odd n = 
    if n = 0 then false 
    else even (n - 1)
```
Here's the translated CPS version:
```
let rec even n k = 
    if n = 0 then k true 
    else odd (n - 1) k 

let rec odd n k = 
    if n = 0 then k false 
    else even (n - 1) k
```
which admittedly, is a bit simpler than the work we had to do before, 
because there is no work after the recursion.

Finally, note that continuation passing style works really well with tail call
optimization.

Consider:
```
let rec length lst acc = 
    match lst with 
    | [] -> acc 
    | _ :: t -> length t (1 + acc)
```
and notice that there is no computation to be done after recursing on t.
Therefore, nothing needs to be added to the continuation. Here is the CPS form:
```
let rec length lst acc k = 
    match lst with 
    | [] -> k acc 
    | _ :: t -> length t (1 + acc) k
```
Simple!

### Translating the Lambda Calculus to CPS

With the above information, we can try to motivate the translation of the CBV lambda calculus to CPS.

This is the standard lambda calculus grammar:
```e ::= x | \x.e  | e0 e1```

Throughout, we assume the standard CBV semantics.

We will formulate the translation in the following manner:
``[[e]] k`` is defined as ```\k. ...```. We further require that every expression
is paired with a continuation that feeds into it, and that every expression ends
computation by sending its value out onto a continuation.

To begin the translation, consider the variable case.

```[[x]] k = k x ```

The translation is like this because in CBV, bound variables have expressions 
substituted into them. Substitution only occurs under evaluation of application.
Therefore, the expression was an argument. But in CBV semantics, arguments are
evaluated to values before substitution. So the expression substituted for x 
is a value. Thus, we apply the continuation k to the value.

Next, consider the abstraction.

```[[\x.e]] k = k (\x. \k'. [[e]] k')```

Notice that ```\x.e``` is a value. Hence the application of k to the abstraction.
Inside is a little tricky. We keep x, the variable, but we also introduce the 
continuation k' that will be passed in for after evaluation of e, which is to be 
used when we apply some expression to this abstraction. Notice we do ```[[e]] k'```.
which is to signal we must evaluate e to a value, before applying k' to it.

Finally, consider the application.

```[[e0 e1]] k = [[e0]](\f. [[e1]] (\v. f v k))```

The translation of this is similar in concept to the translation of addition, keeping in mind the evaluation order of applications. 

In application, we first evaluate e0 to a function f, then evaluate e1 to an argument v,
and then substitute e1 in e0. After all that, we would apply k. This is literally
what the translation says. 

### An Interesting Problem Involving CPS

Can you use fold left to implement fold right? Or vice versa?

Use the definitions of foldl and foldr, written in OCaml.
```
let rec foldl lst f acc = 
    match lst with 
    | [] -> acc 
    | h :: t -> foldl t f (f h acc)
```
and 
```
let rec foldr lst f acc = 
    match lst with 
    | [] -> acc 
    | h :: t -> f h (foldr t f acc)
```

As an aside, here is a cps version of foldr:
```
let rec foldr lst f acc k = 
    match lst with 
    | [] -> k acc 
    | h :: t -> foldr t f acc (\v. k (f h v))
```
which was translated using the exact same ideas that we in the previous sections,
notably that ```foldr t f acc``` needs to be reduced to a value first,
and then after, the continuation should take the value, apply f to the head and the value,
and then throw that value to k.

Notice this translation is tail call optimized! Nothing is done on the stack after
recursion, because instead of returning, we call another function: k.

After the aside, the solution becomes possible to see. As a strategy, we
compare the CPS form of foldr and the direct style foldl function, and jotice 
the code is almost identifical. The only difference is we cannot have
k acc in the foldl function, unlike in the foldr function. Hence, we will have
to throw in acc as an argument at the end. 

Here's the solution:
We match ```(f' h acc)``` with ```(\v. k (f h v)``` in the following way:
Let ```f' = fun h -> fun k -> fun foldr_val -> k (f h foldr_val)```
and we see that ```(f' h acc)``` becomes ```fun foldr_val -> k (f h foldr_val)```
which exactly matches ```(\v. k (f h v)``` from foldr's CPS form. 

Next, for parament named acc, which is now the continuation we pass in the identity, ```fun x -> x```.
Finally, we apply the foldl to the old acc. 

Written out, we have equationally:
```
foldr lst f acc = (foldl lst (fun h -> fun k -> fun v -> k (f h v)) (fun x -> x)) acc
```

The power is that now, we can change control flow to be harnessed in the way we want
it to be, by always passing to another function in the order we want. This is why
continuations are so useful.

As an aside, this solution feels like foldl has been hijacked to make it do foldr's bidding.
I wonder if in general, code could be hijacked in a similar way to act in different ways,
by passing in well-crafted continuation arguments, a la CS3410 stack overflow style.

### Translating a subset of Scheme to CPS

### An introduction to Call/CC

Here's the details for call/cc, directly taken from Wikipedia. 
```(call/cc f)``` is embedded in some expression. The result is f applied to the 
continuation of that expression.
For example, suppose we have ```(e1 (call/cc f))```.
The continuation of the ```(call/cc f)``` expression is ```(lambda (c) (e1 c))```, since
if we substitute ```(call/cc f)``` for c, we get ```(e1 (call/cc f))```.
The result of call/cc is then ```(f (lambda (c) (e1 c)))```.
Next, suppose we had ```((call/cc f) e2)```. The continuation of e2 is ```(lambda (c) (c e2))```, 
since this would apply ```(call/cc f)``` to e2 and we have the result of call/cc as ```(f (lambda (c) (c e2)))```.

Consider the example:
```
(define (f return)
    (return 2)
    3)
```

and we can try
```
(display (f (lambda (x) x)))
```
which prints to output the value 3. 

But if we try 
```
(display (call/cc f))
```
We see that the form is 
```
(e1 (call/cc f))
```
and so we have the result will be 
```
(f (lambda (c) (display c)))
```
which reduces to 
```
(((lambda (c) (display c)) 2) 
    3)
```
which further reduces to 
```
((display 2)
    3)
```
which prints out 2 to standard output.

### Implementing call/cc
