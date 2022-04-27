type lambda = Int | Var | Abs of string * lambda | App of lambda * lambda

let rec static_scope = ()
let rec dynamic_scope = ()