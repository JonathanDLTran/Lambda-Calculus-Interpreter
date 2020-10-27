type lambda = 
  | Fun of char * lambda
  | Var of char
  | App of lambda * lambda

let alpha_eq e1 e2 = 
  failwith "unimplemented"

let rec beta_reduce x e1 e2 = 
  failwith "Unimplemented"

let rec cbn e = 
  match e with 
  | _ -> failwith "Unimplemented"