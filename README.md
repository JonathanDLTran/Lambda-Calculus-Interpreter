# Lambda-Calculus-Interpreter
Lambda Calculus Intepreter, an application of CS 4110 studies

There are several interpreters in this repository.

There are Call By Name and Call By Value interpreters for the Lambda calculus, using De Bruijn Notation. 

There is a Typed Pi Calculus and non-typed Pi Calculus interpreter. 

There is a Scheme/Racket interpreter in these files. Some of the operations may be specific to Racket. The interpreter was built for me to understand Racket quickly, so that I could get used to some work that I was working on at the time. I try to be as faithful to the LISP idea that data is a program and vice versa in the interpreter. Thus, the end goal is to be able to eval the program data at the same time it is running. First class continuations may also be added, if I can figure out a way to create them. 

Following the idea that program is equivalent to data, I have added non-standard parsing for dot notation, that parses it as Cons pairs only, and in all applicable situations, unlike the equivalent in Racket or Scheme. To do infix dot notation, instead, wrap the function in dollar signs, e.g. ```(1 $x$ 1)``` to get ```(+ 1 2)``` or ```(1 $-$ 2 $-$ 3)``` to get ```(- 1 2 3)```. The parsing is recursive, but simple, so there is no operator precedence and it must be completely shown with parentheses. 

Note that virtually everything in the Scheme/Racket interpreter is represented as a list in Python.

Most of the obvious features for Scheme has been added like, '  @ and , for quoting forms.

I have also added a few extra forms as "native" forms to the interpreter, like map. Note that these could be defined as macros, because define-macro is itself a form implemented in the interpreter. However, I implemented define-macro most recently, so it was nicer to test with some externs already preloaded, like map. 

The next step will be to understand continuations, especially call/cc, do some translations to continuation passing form, and add in call/cc. This next step will likely not occur in the nearby future; hopefully it can be done soon.  I will likely start by translating simple parts of the Scheme language, beginning with applications and function definitions,following lecture notes from Cornell's CS 6110 course. 

I've also been meaning to play around with intermediate representations, ASTs, control flow graph generation, and various optimizations on the the control flow graph. Work on that will probably occur over the summer, on a predefined AST that I have been using. As a start, I'd like to be able to generate control flow graphs for the language I created, and add on simple optimizations like dead code elimination for obvious things like returns, breaks and continues, constant propagation and constant folding, and other optimizations like these. After, I would probably pursue more complex optimizations like conditional or loop related optimizations. 

To Run the Scheme Interpreter, make sure Python3 is installed, prefereably 3.7 or higher.

run ```python3 scheme.py``` to start the repl. You will have to have pulled scheme.py and eval.py for it to work. 

For the OCaml programs, compile normally and run the generated binaries. 
