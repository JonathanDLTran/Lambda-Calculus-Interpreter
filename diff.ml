(* Attribution: CS 3110 Fall 2008. *)

(* abstract syntax tree *)
(* Binary Operators *)
type bop = Add | Sub | Mul | Div | Pow

(* Unary Operators *)
type uop = Sin | Cos | Ln | Neg

type expression = Num of float
                | Var
                | BinOp of bop * expression * expression
                | UnOp of uop * expression